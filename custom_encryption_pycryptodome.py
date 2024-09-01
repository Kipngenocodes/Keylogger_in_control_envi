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
        ls = os.urandom(16)
        cipher = AES.new(self.key, AES.MODE_CBC, ls)
        
        # padding the plaintext to a multiple of the AES block size and encrypting it
        padded_text = pad(plaintext.encode(), AES.block_size)
        ciphertext = cipher.encrypt(padded_text)
        
        # returning a dictionary containing cipher text, ls, and salt encoded in base64
        return {
            "ciphertext": base64.b64encode(ciphertext).decode('utf-8'),
            "ls": base64.b64encode(ls).decode('utf-8'),
            "salt": base64.b64encode(self.salt).decode('utf-8')
            }
    # decrytion function 
    def decrypt(self, encrypted_message:dict)-> str:
        # decoding the base64 encoded data
        ciphertext = base64.b64decode(encrypted_message['ciphertext'])
        ls = base64.b64decode(encrypted_message['ls'])
        
        # recreation  of the AES cipher object for decryption
        cipher = AES.new(self.key, AES.MODE_CBC, ls)
        
        # decryptio and then unadding the plain text
        padded_text =cipher.decrypt(ciphertext)
        plaintext = unpad(padded_text, AES.block_size)
        
        return plaintext.decode('utf-8')
    
    
# using the above code
if __name__ == "__main__":
    # creating an instance of the CustomEncryptionTool class
    encryption_tool = CustomEncryptionTool('mysecretpassword')
    
        
        
