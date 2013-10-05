import atexit
from daemon import Daemon
import dbmanager
from settings import CONFIG_CURSOR

__author__ = 'Terry Chia'


class Watcher(Daemon):
    def run(self):
            @atexit.register
            def save_cursor():
                if db.cursor is not None:
                    with open(CONFIG_CURSOR, 'w') as f:
                        f.write(db.cursor)

            db = dbmanager.DropboxManager()
            db.monitor()