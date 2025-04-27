import asyncio
import logging
import os
import random
import time
from telethon import TelegramClient, events, types
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
import pytz
from datetime import datetime
from config import load_env_variables
from telegram_client import client, monitor_target_status, send_scheduled_messages
from flask_server import keep_alive

# Load environment variables
load_env_variables()

# Configs
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
channel_id = os.getenv('CHANNEL_ID')
TARGET_USERNAME = "username"  # The username we want to monitor

# Time configs for India timezone
INDIA_TZ = pytz.timezone('Asia/Kolkata')
MORNING_HOUR = 7  # 7 AM IST
NIGHT_HOUR = 22   # 10 PM IST

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add delays to prevent spam detection
MESSAGE_DELAY = 3  # Seconds between messages
FLOOD_WAIT_DELAY = 60  # Seconds to wait after flood warning
MAX_MESSAGES_PER_MINUTE = 20

# Status tracking variables
was_online = False
online_time = None
last_seen = None
last_message_time = 0
message_count = 0

# Flask server for keeping alive
app = Flask('')


@app.route('/')
def home():
    return "🤖 Status Monitor Bot is Active!"


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


def format_duration(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds) // 60
        return f"{minutes} minutes"
    else:
        hours = int(seconds) // 3600
        minutes = (int(seconds) % 3600) // 60
        return f"{hours} hours {minutes} minutes"


async def format_last_seen(last_seen_date):
    if isinstance(last_seen_date, types.UserStatusOnline):
        return "online"
    elif isinstance(last_seen_date, types.UserStatusOffline):
        timestamp = last_seen_date.was_online
        now = datetime.now(timestamp.tzinfo)
        diff = now - timestamp
        return format_duration(diff.total_seconds()) + " ago"
    return "unknown"


async def safe_send_message(message):
    global last_message_time, message_count
    
    current_time = time.time()
    
    # Check message rate limits
    if current_time - last_message_time < MESSAGE_DELAY:
        await asyncio.sleep(MESSAGE_DELAY)
    
    # Reset counter every minute
    if current_time - last_message_time > 60:
        message_count = 0
    
    # Check if we're within safe limits
    if message_count >= MAX_MESSAGES_PER_MINUTE:
        logger.warning("Message limit reached, waiting...")
        await asyncio.sleep(FLOOD_WAIT_DELAY)
        message_count = 0
    
    try:
        await client.send_message(channel_id, message)
        last_message_time = time.time()
        message_count += 1
        logger.info(f"Sent message: {message}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        await asyncio.sleep(FLOOD_WAIT_DELAY)

async def main():
    await client.start()
    logger.info(f"Bot started! Monitoring @{TARGET_USERNAME}")

    # Give Telegram client some time to initialize
    await asyncio.sleep(2)

    # Run both monitoring and scheduled messages
    await asyncio.gather(
        monitor_target_status(),
        send_scheduled_messages()
    )


if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
