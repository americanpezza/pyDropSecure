import os,  aes
from getpass import getpass
from settings import APP_PATH, CONFIG_PATH, CONFIG_DB, config
from pbkdf2 import PBKDF2


def getCrypticle(pwd,  salt):
    key = PBKDF2(pwd, salt).read(48).encode("base64").replace("\n", "")
    crypt = aes.Crypticle(key)
    
    return crypt

def saveConfiguration(output_path,  pwd = None):
    password = pwd
    if password is None:
        password = getpass('Enter your master password: ')

    salt = os.urandom(8)
    crypt = getCrypticle(password,  salt)
    encrypted = crypt.dumps(config)
    
    with open(output_path, 'wb') as f:
        f.write(salt + encrypted)
    
def loadConfiguration(input_path,  pwd = None):
    password = pwd
    if password is None:
        password = getpass('Enter your master password: ')
	print "Password is '%s', %d" % (password, len(password))

    with open(input_path, 'rb') as f:
        salt = f.read(8)
        encrypted_text = f.read()

    crypt = getCrypticle(password,  salt)
    config = crypt.loads(encrypted_text)

    crypt = getCrypticle(password, config['appSecret'])
    
    return config, crypt
