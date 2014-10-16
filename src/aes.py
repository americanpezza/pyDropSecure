import cPickle as pickle
import hashlib
import hmac
import os
from Crypto.Cipher import AES


class AuthenticationError(Exception):
    pass

class Crypticle(object):
    """Authenticated encryption class

    Encryption algorithm: AES-CBC
    Signing algorithm: HMAC-SHA256
    
    Adapted from http://code.activestate.com/recipes/576980-authenticated-encryption-with-pycrypto/
    and contributions from https://groups.google.com/forum/#!topic/comp.lang.python/Ju8t6DxaAzc 
    
    Handle large files encryption (=by encrypting blocks of file), considering hmac incremental updates
    ref.: http://stackoverflow.com/questions/15034267/hmac-sha256-with-aes-256-in-cbc-mode
    """

    PICKLE_PAD = "pickle::"
    AES_BLOCK_SIZE = 16
    SIG_SIZE = hashlib.sha256().digest_size
    KEY_SIZE = 128

    def __init__(self, key_string, key_size=KEY_SIZE):
        self.keys = self.extract_keys(key_string, key_size)
        self.key_size = key_size

    @classmethod
    def generate_key_string(cls, key_size=KEY_SIZE):
        key = os.urandom(key_size / 8 + cls.SIG_SIZE)
        
        return key.encode("base64").replace("\n", "")

    @classmethod
    def extract_keys(cls, key_string, key_size):
        key = key_string.decode("base64")
        assert len(key) == key_size / 8 + cls.SIG_SIZE, "invalid key"
        
        return key[:-cls.SIG_SIZE], key[-cls.SIG_SIZE:]

    def encrypt(self, data,  progressiveHMAC=None):
        """encrypt data with AES-CBC and sign it with HMAC-SHA256"""
        
        aes_key, hmac_key = self.keys
        pad = self.AES_BLOCK_SIZE - len(data) % self.AES_BLOCK_SIZE
        data += pad * chr(pad)
        iv_bytes = os.urandom(self.AES_BLOCK_SIZE)
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = iv_bytes + cypher.encrypt(data)
        
        if progressiveHMAC is not None:
            progressiveHMAC.update(data)
            sig = progressiveHMAC.digest()
        else:
            sig = hmac.new(hmac_key, data, hashlib.sha256).digest()
        
        return data + sig

    def decrypt(self, data):
        """verify HMAC-SHA256 signature and decrypt data with AES-CBC"""
        
        aes_key, hmac_key = self.keys
        
        sig = data[-self.SIG_SIZE:]
        data = data[:-self.SIG_SIZE]

        #
        # if hmac.new(hmac_key, data, hashlib.sha256).digest() != sig:
        #
        # use compare_digest() instead of a == b to prevent timing analysis
        # ref https://docs.python.org/2/library/hmac.html
        dataSig = hmac.new(hmac_key, data, hashlib.sha256)
        if  not dataSig.compare_digest(dataSig.digest(),  sig):
            raise AuthenticationError("message authentication failed")
            
        iv_bytes = data[:self.AES_BLOCK_SIZE]
        data = data[self.AES_BLOCK_SIZE:]
        cypher = AES.new(aes_key, AES.MODE_CBC, iv_bytes)
        data = cypher.decrypt(data)
        
        return data[:-ord(data[-1])]

    def dumps(self, obj, pickler=pickle):
        """pickle and encrypt a python object"""
        
        return self.encrypt(self.PICKLE_PAD + pickler.dumps(obj))

    def loads(self, data, pickler=pickle):
        """decrypt and unpickle a python object"""
        
        data = self.decrypt(data)
        # simple integrity check to verify that we got meaningful data
        assert data.startswith(self.PICKLE_PAD), "unexpected header"
        
        return pickler.loads(data[len(self.PICKLE_PAD):])
