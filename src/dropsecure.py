#!/usr/bin/env python

import argparse
import os,  sys
import configure
from settings import APP_PATH, CONFIG_DB,  config
import watcher
import dbmanager

__author__ = 'Terry Chia'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--start', help='Start the script',
                        action='store_true')
    action.add_argument('--stop', help='Stop the script',
                        action='store_true')
    action.add_argument('--restart', help='Restart the script',
                        action='store_true')
    action.add_argument('--export', help='Export application keys')
    action.add_argument('--import', help='Import application keys',
                        dest='imp')
    action.add_argument('--configure', help='Configure the application',
                        action='store_true')
    args = parser.parse_args()

    if args.export is not None:
        configure.export_configuration(args.export)

    elif args.imp is not None:
        configure.import_configuration(args.imp)

    elif args.configure:
        if not os.path.exists(APP_PATH):
            os.makedirs(APP_PATH)

        choice = "Y"
        if os.path.exists(CONFIG_DB):
            while 1:
                choice = raw_input('Configuration file exists. '
                                   'Do you want to overwrite? (Y/n)')

                if choice == 'Y' or choice == 'n':
                    break
 
        if choice == 'Y':
            configure.new_configuration()

    else:
        db = dbmanager.DropboxManager()

        if args.start:
            daemon = watcher.Watcher(db, '/tmp/dropsecure.pid')
            daemon.start()

        elif args.stop:
            daemon = watcher.Watcher(db, '/tmp/dropsecure.pid')
            daemon.stop()

        elif args.restart:
            daemon = watcher.Watcher(db, '/tmp/dropsecure.pid')
            daemon.restart()
        
