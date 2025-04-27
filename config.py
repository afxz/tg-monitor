import os
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    global api_id, api_hash, channel_id, TARGET_USERNAME
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    channel_id = os.getenv('CHANNEL_ID')
    TARGET_USERNAME = "username"