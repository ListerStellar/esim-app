import jwt
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import os

from database.db import get_session

KEYS_DIR = os.getenv("KEYS_DIR", "/app/keys")
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")
INTERNAL_TOKEN_PATH = os.path.join(KEYS_DIR, "internal_token.txt")

# Load RSA Keys
if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
    raise RuntimeError(f"RSA keys not found in {KEYS_DIR}. Did you run generate_keys.py?")

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

# Load Internal API Token
env_token = os.getenv("INTERNAL_API_TOKEN")
if env_token:
    INTERNAL_API_TOKEN = env_token
else:
    if not os.path.exists(INTERNAL_TOKEN_PATH):
        raise RuntimeError(f"Internal API token not found in {KEYS_DIR}. Did you run generate_keys.py?")
    with open(INTERNAL_TOKEN_PATH, "r") as f:
        INTERNAL_API_TOKEN = f.read().strip()


ALGORITHM = "RS256"

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

class JWTUser(BaseModel):
    id: int
    email: str | None = None

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> JWTUser:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise credentials_exception
            
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
            
        try:
            user_id = int(user_id_str)
        except ValueError:
            raise credentials_exception
            
        email = payload.get("email")
        
    except jwt.PyJWTError:
        raise credentials_exception
        
    return JWTUser(id=user_id, email=email)
