import os
import dropbox
import sqlite3
import aes
from settings import APP_PATH, APP_KEY, APP_SECRET, CONFIG_PATH, CONFIG_DB


__author__ = 'Terry Chia'

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
