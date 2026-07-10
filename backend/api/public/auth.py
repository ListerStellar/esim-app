from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr
import hashlib
import hmac
import os
import secrets
import string
import base64
from datetime import datetime, timedelta, timezone

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers

from database.db import get_session, User, RefreshToken
from auth.security import get_password_hash, verify_password, create_access_token, PUBLIC_KEY

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    referral_code: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class TelegramLoginRequest(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: int
    hash: str

def generate_referral_code():
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))

async def create_tokens_for_user(user: User, session: AsyncSession) -> TokenResponse:
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    
    plain_refresh_token = secrets.token_urlsafe(64)
    hashed_refresh_token = hashlib.sha256(plain_refresh_token.encode()).hexdigest()
    
    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    
    db_token = RefreshToken(
        user_id=user.id,
        token=hashed_refresh_token,
        expires_at=expires_at
    )
    session.add(db_token)
    await session.commit()
    
    return TokenResponse(access_token=access_token, refresh_token=plain_refresh_token)

@router.post("/register", response_model=TokenResponse)
async def register(req: RegisterRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.email == req.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")

    referred_by_id = None
    if req.referral_code:
        ref_res = await session.execute(select(User).filter(User.referral_code == req.referral_code))
        ref_user = ref_res.scalars().first()
        if ref_user:
            referred_by_id = ref_user.id

    new_user = User(
        email=req.email,
        hashed_password=get_password_hash(req.password),
        referral_code=generate_referral_code(),
        referred_by=referred_by_id,
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return await create_tokens_for_user(new_user, session)


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")
        
    return await create_tokens_for_user(user, session)


@router.post("/telegram", response_model=TokenResponse)
async def login_via_telegram(req: TelegramLoginRequest, session: AsyncSession = Depends(get_session)):
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise HTTPException(status_code=500, detail="Bot token not configured")
        
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(req.model_dump(exclude={"hash"}, exclude_none=True).items())
    )
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    if expected_hash != req.hash:
        raise HTTPException(status_code=401, detail="Invalid Telegram authentication")
        
    result = await session.execute(select(User).filter(User.telegram_id == req.id))
    user = result.scalars().first()
    
    if not user:
        name_parts = [req.first_name]
        if req.last_name:
            name_parts.append(req.last_name)
        full_name = " ".join(name_parts)
        
        user = User(
            telegram_id=req.id,
            username=req.username,
            full_name=full_name,
            referral_code=generate_referral_code()
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
    if user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned")
        
    return await create_tokens_for_user(user, session)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(req: RefreshRequest, session: AsyncSession = Depends(get_session)):
    hashed_token = hashlib.sha256(req.refresh_token.encode()).hexdigest()
    
    result = await session.execute(
        select(RefreshToken).filter(RefreshToken.token == hashed_token)
    )
    db_token = result.scalars().first()
    
    if not db_token or db_token.revoked or db_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
        
    user_res = await session.execute(select(User).filter(User.id == db_token.user_id))
    user = user_res.scalars().first()
    
    if not user or user.is_banned:
        raise HTTPException(status_code=403, detail="User is banned or does not exist")
        
    # Rotate token: revoke old
    db_token.revoked = True
    await session.commit()
    
    # Issue new pair
    return await create_tokens_for_user(user, session)


@router.post("/logout")
async def logout(req: RefreshRequest, session: AsyncSession = Depends(get_session)):
    hashed_token = hashlib.sha256(req.refresh_token.encode()).hexdigest()
    
    result = await session.execute(
        select(RefreshToken).filter(RefreshToken.token == hashed_token)
    )
    db_token = result.scalars().first()
    
    if db_token:
        db_token.revoked = True
        await session.commit()
        
    return {"detail": "Successfully logged out"}


def int_to_base64url(val: int) -> str:
    val_bytes = val.to_bytes((val.bit_length() + 7) // 8, byteorder="big")
    return base64.urlsafe_b64encode(val_bytes).rstrip(b"=").decode("ascii")

@router.get("/.well-known/jwks.json")
async def get_jwks():
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.backends import default_backend

    public_key_obj = serialization.load_pem_public_key(PUBLIC_KEY, backend=default_backend())
    numbers = public_key_obj.public_numbers()
    
    return {
        "keys": [
            {
                "kty": "RSA",
                "alg": "RS256",
                "use": "sig",
                "kid": "main-key",
                "n": int_to_base64url(numbers.n),
                "e": int_to_base64url(numbers.e),
            }
        ]
    }
