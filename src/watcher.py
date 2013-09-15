import atexit
from config import CONFIG_CURSOR
import dbmanager

__author__ = 'Terry Chia'

if __name__ == '__main__':
    @atexit.register
    def save_cursor():
        if db.cursor is not None:
            with open(CONFIG_CURSOR, 'w') as f:
                f.write(db.cursor)

    db = dbmanager.DropboxManager()
    db.monitor()