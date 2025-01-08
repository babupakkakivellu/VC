import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, InputAudioStream, InputVideoStream
from pytgcalls.types.stream import StreamAudioEnded
from pyrogram.types import Message

# Telegram API credentials
API_ID = 1234567  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API Hash
BOT_TOKEN = "your_bot_token"  # Replace with your Bot Token

app = Client("vc_player_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# Active streams tracking
active_streams = {}

@app.on_message(filters.command("vplay") & filters.reply)
async def vplay_handler(client: Client, message: Message):
    """Stream a video in the voice chat."""
    chat_id = message.chat.id
    
    # Check if already streaming
    if chat_id in active_streams:
        await message.reply("A stream is already active! Use /vstop to stop it first.")
        return
    
    # Ensure reply is a video message
    if not message.reply_to_message or not message.reply_to_message.video:
        await message.reply("Reply to a video file with /vplay to stream it in the voice chat.")
        return

    # Download the video file
    video_file = await message.reply_to_message.download()
    try:
        # Start the video stream
        await pytgcalls.join_group_call(
            chat_id,
            InputStream(
                InputAudioStream(video_file),
                InputVideoStream(video_file),
            ),
        )
        active_streams[chat_id] = video_file
        await message.reply("🎥 Streaming started!")
    except Exception as e:
        await message.reply(f"❌ Failed to start streaming: {e}")
        if os.path.exists(video_file):
            os.remove(video_file)

@app.on_message(filters.command("vstop"))
async def vstop_handler(client: Client, message: Message):
    """Stop the active stream in the voice chat."""
    chat_id = message.chat.id

    if chat_id not in active_streams:
        await message.reply("No active stream to stop.")
        return

    try:
        # Leave the group call and clean up
        await pytgcalls.leave_group_call(chat_id)
        video_file = active_streams.pop(chat_id)
        if os.path.exists(video_file):
            os.remove(video_file)
        await message.reply("⏹ Stream stopped.")
    except Exception as e:
        await message.reply(f"❌ Failed to stop streaming: {e}")

@pytgcalls.on_stream_end()
async def handle_stream_end(client, update: StreamAudioEnded):
    """Automatically clean up when a stream ends."""
    chat_id = update.chat_id
    if chat_id in active_streams:
        video_file = active_streams.pop(chat_id)
        if os.path.exists(video_file):
            os.remove(video_file)
        await app.send_message(chat_id, "🔴 Stream ended automatically.")

async def main():
    """Start the bot and PyTgCalls."""
    await app.start()
    await pytgcalls.start()
    print("Bot is up and running!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
  
