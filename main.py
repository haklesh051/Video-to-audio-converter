from pyrogram import Client, filters
from gtts import gTTS
import os
import asyncio
import uuid

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("caption_audio_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.video)
async def handle_video(client, message):
    caption = message.caption
    if not caption:
        await message.reply("⚠️ Video has no caption.")
        return

    temp_filename = f"{uuid.uuid4().hex}.mp3"
    await message.reply("🔊 Converting caption to audio...")

    try:
        tts = gTTS(caption, lang="hi")  # Change to 'en' if caption is English
        tts.save(temp_filename)

        await message.reply_audio(audio=temp_filename, caption="🎧 Caption to audio")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Send me a video (with caption), and I’ll send audio of the caption.\nYou can send multiple videos one by one.")

app.run()
