"""Configuration module for Server Activity Monitor"""
import os
import json
from pathlib import Path

# Application paths
APP_DATA_DIR = Path(os.path.expandvars(r'%APPDATA%\ServerActivityMonitor'))
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

USER_CONFIG_FILE = APP_DATA_DIR / 'user_config.json'
MESSAGES_DB = APP_DATA_DIR / 'messages.db'

# Network settings
BROADCAST_PORT = 27001
BROADCAST_ADDRESS = '255.255.255.255'
BROADCAST_TIMEOUT = 2  # seconds
DISCOVERY_INTERVAL = 5  # seconds between discovery broadcasts
MESSAGE_PORT = 27002

# Application settings
APP_NAME = 'Server Activity Monitor'
APP_VERSION = '1.0.0'
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300

# Server statuses
STATUS_NEED_SERVER = 'I need the server'
STATUS_USING_SERVER = 'I\'m using the server'
STATUS_DONE_SERVER = 'I\'m done using the server'

VALID_STATUSES = [STATUS_NEED_SERVER, STATUS_USING_SERVER, STATUS_DONE_SERVER]

def get_user_name():
    """Get saved user name from config"""
    if USER_CONFIG_FILE.exists():
        try:
            with open(USER_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('username')
        except Exception:
            pass
    return None

def save_user_name(username):
    """Save user name to config"""
    config = {'username': username}
    try:
        with open(USER_CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return True
    except Exception as e:
        print(f"Error saving user name: {e}")
        return False
