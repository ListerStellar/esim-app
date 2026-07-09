from fastapi import FastAPI, Depends, HTTPException, Header
from database.db import init_db
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="eSIM Store API")

INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "super-secret-internal-token")

async def verify_internal_token(x_internal_token: str = Header(...)):
    if x_internal_token != INTERNAL_API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid internal token")

from api.internal import users, catalog, transactions
from api.public import webhooks

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    await init_db()

app.include_router(users.router, dependencies=[Depends(verify_internal_token)])
app.include_router(catalog.router, dependencies=[Depends(verify_internal_token)])
app.include_router(transactions.router, dependencies=[Depends(verify_internal_token)])
app.include_router(webhooks.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
