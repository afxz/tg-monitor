
# 🤖 Telegram Status Monitor Bot

A Telegram userbot that monitors online/offline status of a target account and sends scheduled motivational messages.

## 🌟 Features

- 📱 **Status Monitoring**: Tracks when a specific Telegram user goes online/offline
- ⏰ **Duration Tracking**: Records how long the user was online
- 🌅 **Scheduled Messages**: 
  - Sends random motivational messages every morning (7 AM IST)
  - Sends good night messages every evening (10 PM IST)
- 🔒 **Safe Operations**: Implements rate limiting and anti-spam measures
- 🌐 **24/7 Operation**: Includes keep-alive mechanism

## 🛠️ Setup

1. Clone the repository
2. Create a `.env` file with the following variables:
```
API_ID=your_api_id
API_HASH=your_api_hash
CHANNEL_ID=your_channel_id
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the bot:
```bash
python main.py
```

The bot will start monitoring the specified target account and send status updates to your designated channel.

## ⚙️ Configuration

- Target username can be modified in `main.py`
- Message templates can be customized in the code
- Scheduling times can be adjusted (default: 7 AM and 10 PM IST)

## 🔐 Safety Features

- Rate limiting for message sending
- Flood protection
- Proper device identification
- Error handling with automatic cooldown

## 📝 License

MIT License

## 🧑‍💻 Developer

[@afxz](https://github.com/afxz)

