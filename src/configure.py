from getpass import getpass
import os
import dropbox
from pbkdf2 import PBKDF2
import crypto
from settings import APP_PATH, CONFIG_PATH, CONFIG_DB, config


__author__ = 'Terry Chia'


def new_configuration():
    if not os.path.exists(APP_PATH):
        os.makedirs(APP_PATH)

    appKey = raw_input('1. Enter your application key: ').strip()
    appSecret = raw_input('2. Enter your application secret: ').strip()
    
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(appKey,  appSecret)
    authorize_url = flow.start()

    print '3. Go to: ' + authorize_url
    print '4. Click "Allow" (you might have to log in first)'
    print '5. Copy the authorization code.'
    code = raw_input("6. Enter the authorization code here: ").strip()
    
    masterPwd = 0
    masterPwdConfirm = None
    
    while (masterPwd != masterPwdConfirm):
        masterPwd = getpass("7. Enter your master password: ")
        masterPwdConfirm = getpass("8. Confirm your master password: ")
        if masterPwd != masterPwdConfirm:
            print "Passwords didn't match. Try again."
            
    config['appKey'] = appKey
    config['appSecret'] = appSecret
    
    token, user_id = flow.finish(code)
    
    config['appToken'] = token
    config['userId'] = user_id
    
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)

    crypto.saveConfiguration(CONFIG_DB,  masterPwd)

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
