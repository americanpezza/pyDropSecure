import os

__author__ = 'Terry Chia'

APP_KEY = "INSERTAPPKEY"
APP_SECRET = "INSERTAPPSECRET"

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.dropsecure')
CONFIG_DB = os.path.join(CONFIG_PATH, 'config.db')
CONFIG_CURSOR = os.path.join(CONFIG_PATH, 'cursor')

APP_PATH = os.path.join(os.path.expanduser('~'), 'DropSecure')