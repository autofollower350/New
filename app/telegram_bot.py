
import asyncio
import os
import nest_asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from app.selenium_bot import start_browser, fetch_result

nest_asyncio.apply()

API_ID = 28590286
API_HASH = "6a68cc6b41219dc57b7a52914032f92f"
BOT_TOKEN = "7412939071:AAFgfHJGhMXw9AuGAAnPuGk_LbAlB5kX2KY"

app = Client("jnvu_result_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    start_browser()
    await message.reply("✅ Bot ready. Send your roll number like `25rba00299`.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def handle_roll_number(client: Client, message: Message):
    roll_number = message.text.strip()
    if not (6 <= len(roll_number) <= 15 and roll_number.isalnum()):
        await message.reply("⚠️ Invalid roll number format.")
        return

    await message.reply("⏳ Fetching result...")
    pdf_path = fetch_result(roll_number)
    if pdf_path and os.path.exists(pdf_path):
        await message.reply_document(pdf_path, caption=f"📄 Result for `{roll_number}`")
    else:
        await message.reply("❌ PDF not found. Please try again later.")
