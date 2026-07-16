from fastapi import FastAPI, Depends, HTTPException, Header
from database.db import init_db
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="eSIM Store API", docs_url="/api/docs", openapi_url="/api/openapi.json")

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from rate_limit import limiter

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В проде здесь должны быть конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from starlette.middleware.sessions import SessionMiddleware
from config import config
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

import hmac
from auth.security import INTERNAL_API_TOKEN

async def verify_internal_token(x_internal_token: str = Header(...)):
    if not hmac.compare_digest(x_internal_token, INTERNAL_API_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid internal token")

from api.internal import users, transactions
from api.public import webhooks, auth_routes, catalog as public_catalog
from api.public import users as public_users
from api.public import transactions as public_transactions

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    await init_db()

app.include_router(users.router, dependencies=[Depends(verify_internal_token)])
app.include_router(transactions.router, dependencies=[Depends(verify_internal_token)])

app.include_router(auth_routes.router, prefix="/api")
app.include_router(public_catalog.router, prefix="/api")
app.include_router(public_users.router, prefix="/api")
app.include_router(public_transactions.router, prefix="/api")
app.include_router(webhooks.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
