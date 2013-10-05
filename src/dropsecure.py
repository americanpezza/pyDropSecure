import argparse
import os
import configure
from settings import APP_PATH, CONFIG_DB
import watcher

__author__ = 'Terry Chia'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    action = parser.add_mutually_exclusive_group()
    action.add_argument('--start', help='Start the script',
                        action='store_true')
    action.add_argument('--stop', help='Stop the script',
                        action='store_true')
    action.add_argument('--restart', help='Restart the script',
                        action='store_true')
    action.add_argument('--export', help='Export application keys',
                        action='store_true')
    action.add_argument('--import', help='Import application keys',
                        action='store_true', dest='imp')
    action.add_argument('--configure', help='Configure the application',
                        action='store_true')
    args = parser.parse_args()

    if args.export:
        print 'Exported'

    elif args.imp:
        print 'Imported'

    elif args.configure:
        if not os.path.exists(APP_PATH):
            os.makedirs(APP_PATH)

        if os.path.exists(CONFIG_DB):
            while 1:
                choice = raw_input('Configuration file exists. '
                                   'Do you want to overwrite? (Y/n)')

                if choice == 'Y':
                    configure.new_configuration()
                    break

                elif choice == 'n':
                    break

                else:
                    pass

        else:
            configure.new_configuration()

    elif args.start:
        daemon = watcher.Watcher('/tmp/dropsecure.pid')
        daemon.start()

    elif args.stop:
        daemon = watcher.Watcher('/tmp/dropsecure.pid')
        daemon.stop()

    elif args.restart:
        daemon = watcher.Watcher('/tmp/dropsecure.pid')
        daemon.restart()

