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

- Target username can be modified in `config.py`
- Message templates can be customized in `message_templates.py`
- Scheduling times can be adjusted (default: 7 AM and 10 PM IST)

## 🔐 Safety Features

- Rate limiting for message sending
- Flood protection
- Proper device identification
- Error handling with automatic cooldown

## 🌍 Deployment on Koyeb

You can deploy this bot on Koyeb for free to keep it running 24/7.

### Steps to Deploy:

1. **Create a Koyeb Account**: Sign up at [Koyeb](https://www.koyeb.com/).
2. **Create a New App**:
   - Select "Deploy from GitHub" and connect your repository.
   - Choose this repository and branch.
3. **Set Environment Variables**:
   - Add the following environment variables in the Koyeb dashboard:
     - `API_ID`
     - `API_HASH`
     - `CHANNEL_ID`
4. **Select Runtime**:
   - Use the Python runtime.
5. **Start the App**:
   - Deploy the app and monitor logs to ensure it starts successfully.

## 📝 License

MIT License

## 🧑‍💻 Developer

[@afxz](https://github.com/afxz)

