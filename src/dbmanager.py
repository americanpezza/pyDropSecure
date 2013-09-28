import hashlib
import os
import shutil
import sqlite3
import dropbox
import time
import aes
from settings import CONFIG_DB, CONFIG_CURSOR, APP_PATH

__author__ = 'ayrx'


class DropboxManager:

    def __init__(self):
        conn = sqlite3.connect(CONFIG_DB)
        c = conn.cursor()

        c.execute('SELECT * FROM token')
        token = c.fetchone()[0]

        c.execute('SELECT * FROM key')
        key = c.fetchone()[0]

        conn.close()

        self.client = dropbox.client.DropboxClient(token)
        self.crypt = aes.Crypticle(key)

        if os.path.exists(CONFIG_CURSOR):
            with open(CONFIG_CURSOR, 'r') as f:
                self.cursor = f.read()
        else:
            self.cursor = None

        self.local_files = {}
        for root, dirs, files in os.walk(APP_PATH):
            for d in dirs:
                self.local_files[os.path.join(root, d)] = None
            for f in files:
                self.local_files[os.path.join(root, f)] = self._md5sum(os.path.join(root, f))

        self.recently_uploaded = []

    def monitor(self):
        while True:
            print 'Cursor is ', self.cursor
            self.get_delta()
            self.upload_new_files()
            time.sleep(10)

    def download(self, path):
        print "Downloading ", path
        f, meta = self.client.get_file_and_metadata(path)
        with open(self._get_absolute_from_relpath(path), 'wb') as foo:
            foo.write(self._decrypt(f.read()))
        f.close()
        self.local_files[self._get_absolute_from_relpath(path)] = self._md5sum(self._get_absolute_from_relpath(path))

    def upload(self, path):
        print "Uploading ", path
        if os.path.isdir(path):
            self.client.file_create_folder(self._get_relpath_from_absolute(path))
        else:
            with open(path, 'rb') as f:
                self.client.put_file(self._get_relpath_from_absolute(path), self._encrypt(f.read()), overwrite=True)

        self.recently_uploaded.append('/' + self._get_relpath_from_absolute(path))

    def remove(self, path):
        print "Removing ", path
        self.client.file_delete(self._get_relpath_from_absolute(path))

    def move(self, src_path, dest_path):
        print "Moving ", src_path, " to ", dest_path
        self.client.file_move(self._get_relpath_from_absolute(src_path),
                              self._get_relpath_from_absolute(dest_path))

    def get_delta(self):
        print "Getting delta"
        tree = {}

        while True:
            result = self.client.delta(self.cursor)

            if result['reset']:
                print 'Delta has been reset'

            for path, metadata in result['entries']:
                if path not in self.recently_uploaded:
                    tree[path] = metadata

            self.cursor = result['cursor']

            if not result['has_more']:
                if tree:
                    self._apply_delta(tree)
                break

        self.recently_uploaded[:] = []

    def _apply_delta(self, tree):
        dirs = []
        files = []

        for key in tree:
            if tree[key] is None:
                self._delete_if_exist(key)
            else:
                meta = tree[key]
                if meta['is_dir']:
                    dirs.append(meta['path'])
                elif not meta['is_dir']:
                    files.append(meta['path'])

        for d in dirs:
            path = self._get_absolute_from_relpath(d)
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                    print "Creating directory ", d
                    os.makedirs(path)
                    self.local_files[path] = None
                else:
                    # Apply the new metadata to the folder,
                    # but do not modify the folders children.
                    pass
            else:
                print "Creating directory ", d
                os.makedirs(path)
                self.local_files[path] = None

        for f in files:
            self._delete_if_exist(f)
            self.download(f)

    def upload_new_files(self):
        filelist = []
        for root, dirs, files in os.walk(APP_PATH):
            for d in dirs:
                filelist.append(os.path.join(root, d))
            for f in files:
                filelist.append(os.path.join(root, f))

        for f in filelist:
            if f not in self.local_files.keys():
                print 'Uploading ', f
                self.upload(f)
                self.local_files[f] = self._md5sum(f)

            elif self._md5sum(f) != self.local_files[f]:
                print 'Uploading ', f
                self.upload(f)
                self.local_files[f] = self._md5sum(f)

        for f in self.local_files.keys():
            if f not in filelist:
                self.remove(f)
                del self.local_files[f]

    def _encrypt(self, data):
        return self.crypt.encrypt(data)

    def _decrypt(self, data):
        return self.crypt.decrypt(data)

    def _get_relpath_from_absolute(self, path):
        return os.path.relpath(path, APP_PATH)

    def _get_absolute_from_relpath(self, path):
        return os.path.join(APP_PATH, path[1:])

    def _delete_if_exist(self, path):
        path = self._get_absolute_from_relpath(path)
        path = self._get_case_sensitive_pathname(path)
        try:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

                del self.local_files[path]

        except OSError:
            pass

    def _get_case_sensitive_pathname(self, path):
        for root, dirs, files in os.walk(APP_PATH):
            for d in dirs:
                if os.path.join(root, d).lower() == path.lower():
                    return os.path.join(root, d)
            for f in files:
                if os.path.join(root, f).lower() == path.lower():
                    return os.path.join(root, f)

        return path

    def _md5sum(self, fname):
        return hashlib.md5(open(fname, 'rb').read()).digest()
