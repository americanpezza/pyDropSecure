import os

__author__ = 'Terry Chia'

config = {
    'appKey': None, 
    'appSecret': None, 
    'appToken': None, 
    'userId': None
}

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.dropsecure')
CONFIG_DB = os.path.join(CONFIG_PATH, 'config.db')
CONFIG_CURSOR = os.path.join(CONFIG_PATH, 'cursor')

APP_PATH = os.path.join(os.path.expanduser('~'), 'DropSecure')
