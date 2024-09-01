from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import os
import base64


#Creating a class called Custom Encryption Tool
class CustomEncryptionTool:
    def __init__(self, password: str, salt: bytes = None):
        # generating salt if not provided
        self.salt = salt if salt else os.urandom(16)
        # key derivation using PBKDF2 with HMAC-SHA256
        self.key = PBKDF2(password, self.salt,dkLen=32, count=100000)
        
    # creating a encrypt function 
    def encrypt(self, plaintext: str) -> dict:
        