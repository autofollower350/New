
from fastapi import FastAPI
import asyncio
from app.telegram_bot import app as telegram_app

fastapi_app = FastAPI()

@fastapi_app.on_event("startup")
async def on_startup():
    print("🚀 Starting Telegram bot...")
    await telegram_app.start()
    asyncio.create_task(telegram_app.idle())
