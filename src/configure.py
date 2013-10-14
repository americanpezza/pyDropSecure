from getpass import getpass
import os
import dropbox
import sqlite3
from pbkdf2 import PBKDF2
import aes
from settings import APP_PATH, APP_KEY, APP_SECRET, CONFIG_PATH, CONFIG_DB


__author__ = 'Terry Chia'


def new_configuration():
    if not os.path.exists(APP_PATH):
        os.makedirs(APP_PATH)

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    authorize_url = flow.start()
    print '1. Go to: ' + authorize_url
    print '2. Click "Allow" (you might have to log in first)'
    print '3. Copy the authorization code.'
    code = raw_input("Enter the authorization code here: ").strip()

    access_token, user_id = flow.finish(code)

    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)

    conn = sqlite3.connect(CONFIG_DB)
    c = conn.cursor()
    c.execute('CREATE TABLE token (token text)')
    c.execute('CREATE TABLE key (key text)')
    c.execute('INSERT INTO token VALUES (?)', (access_token, ))
    c.execute('INSERT INTO key VALUES(?)', (aes.Crypticle.generate_key_string(), ))
    conn.commit()
    conn.close()


def export_configuration(output_path):
    password = getpass('Please enter password to encrypt exported file with: ')
    salt = os.urandom(8)
    key = PBKDF2(password, salt).read(48).encode("base64").replace("\n", "")
    crypt = aes.Crypticle(key)

    with open(CONFIG_DB, 'rb') as f:
        foo = crypt.encrypt(f.read())

    with open(output_path, 'wb') as f:
        f.write(salt+foo)


def import_configuration(input_path):
    password = getpass('Please enter password to decrypt file to import: ')

    with open(input_path, 'rb') as f:
        salt = f.read(8)
        encrypted_text = f.read()

    key = PBKDF2(password, salt).read(48).encode("base64").replace("\n", "")
    crypt = aes.Crypticle(key)

    with open(CONFIG_DB, 'wb') as f:
        f.write(crypt.decrypt(encrypted_text))
