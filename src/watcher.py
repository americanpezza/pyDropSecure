import atexit
from daemon import Daemon
from settings import CONFIG_CURSOR

__author__ = 'Terry Chia'


class Watcher(Daemon):
    def __init__(self,  db,  *args,  **kwargs):
        Daemon.__init__(self,  *args,  **kwargs)
        self.db = db
        
    def run(self):
            @atexit.register
            def save_cursor():
                if self.db.cursor is not None:
                    with open(CONFIG_CURSOR, 'w') as f:
                        f.write(self.db.cursor)

            self.db.monitor()
