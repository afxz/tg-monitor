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

# Load environment variables
load_dotenv()

# Configs
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
channel_id = os.getenv('CHANNEL_ID')
TARGET_USERNAME = "username"  # The username we want to monitor

# Time configs for India timezone
INDIA_TZ = pytz.timezone('Asia/Kolkata')
MORNING_HOUR = 7  # 7 AM IST
NIGHT_HOUR = 22   # 10 PM IST

# Message Templates
motivational_messages = [
    "🌅 Rise and shine! Today is a new beginning! ✨",
    "🎯 You've got this! Make today amazing! 💪",
    "🌟 Every day is a fresh start! Believe in yourself! ⭐",
    "🚀 Dream big, work hard, stay focused! 💫",
    "🌈 Your potential is limitless! Keep going! 🔥",
    "🎨 Create the life you dream about! ✨",
    "🌞 Today's a gift, that's why it's called present! 🎁"
]

goodnight_messages = [
    "🌙 Sweet dreams! Rest well for another amazing day! ✨",
    "🌟 Time to recharge for tomorrow's adventures! 💫",
    "🌃 Wishing you a peaceful night's sleep! 😴",
    "✨ Good night! Let your dreams take flight! 🦋",
    "🌠 Sleep tight! Tomorrow will be bright! 💫",
    "🌜 Rest well and dream big! ⭐",
    "🎆 Another day well spent! Sweet dreams! 💤"
]

online_messages = [
    "✅ 💎 User is now online!",
    "🌟 Heads up everyone, User just appeared!",
    "🎉 Party time, User is online!",
    "🪩 User is shining online right now!",
    "💬 User is here to vibe!",
]

offline_messages = [
    "❌ 💎 User went offline after {duration}. See you soon!",
    "🌙 User left after {duration}. Take Care!",
    "👋 User logged off after {duration}. Catch you later!",
    "✨ User was online for {duration}. Good times!",
    "📴 User logged out after {duration}.",
    "🌟 User's vibe is on pause after {duration}.",
]

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Telegram Client with safety settings
client = TelegramClient('userbot_session', api_id, api_hash, 
    device_model="Pixel 7",  # Use common device name
    system_version="Android 13",
    app_version="9.6.3",  # Use stable Telegram version
    flood_sleep_threshold=60  # Pause on flood wait
)

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


async def monitor_target_status():
    global was_online, online_time

    # Initial target user lookup
    try:
        target_user = await client.get_entity(TARGET_USERNAME)
        logger.info(f"Found target user: @{TARGET_USERNAME}")
    except ValueError as e:
        logger.error(
            f"Could not find user @{TARGET_USERNAME}. Please check if the username is correct."
        )
        return

    while True:
        try:
            # Get fresh status
            target_user = await client.get_entity(target_user)
            current_status = target_user.status

            # Only track target's status changes
            if isinstance(current_status,
                          types.UserStatusOnline) and not was_online:
                was_online = True
                online_time = time.time()
                msg = random.choice(online_messages)
                await safe_send_message(msg)
                logger.info(f"Target status update: {msg}")

            elif not isinstance(current_status,
                                types.UserStatusOnline) and was_online:
                was_online = False
                duration = format_duration(time.time() - online_time)
                msg = random.choice(offline_messages).format(duration=duration)
                await safe_send_message(msg)
                logger.info(f"Target status update: {msg}")

        except Exception as e:
            logger.error(f"Error monitoring target status: {e}")

        await asyncio.sleep(5)


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

async def send_scheduled_messages():
    while True:
        try:
            # Get current time in IST
            now = datetime.now(INDIA_TZ)
            current_hour = now.hour

            # Send morning motivation
            if current_hour == MORNING_HOUR and now.minute == 0:
                msg = random.choice(motivational_messages)
                await safe_send_message(msg)

            # Send good night
            if current_hour == NIGHT_HOUR and now.minute == 0:
                msg = random.choice(goodnight_messages)
                await safe_send_message(msg)

            # Wait for next minute
            await asyncio.sleep(60)

        except Exception as e:
            logger.error(f"Error sending scheduled message: {e}")
            await asyncio.sleep(60)

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
