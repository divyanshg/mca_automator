import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import urllib.parse

# Constants
password = "d6163f0659cfe4196dc03c2c29aab06f10cb0a79cdfc74a45da2d72358712e80"
salt = hashlib.md5("fc74a45dsalt".encode()).digest()
iv = hashlib.md5("c29aab06iv".encode()).digest()
key_size = 128
iterations = 100

def derive_key(password, salt, key_size, iterations):
    return PBKDF2(password.encode(), salt, dkLen=key_size//8, count=iterations)

def encrypt(plaintext):
    key = derive_key(password, salt, key_size, iterations)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return urllib.parse.quote(base64.b64encode(encrypted).decode())

def decrypt(ciphertext):
    key = derive_key(password, salt, key_size, iterations)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decoded = base64.b64decode(urllib.parse.unquote(ciphertext))
    decrypted = cipher.decrypt(decoded)
    return unpad(decrypted, AES.block_size).decode()

# Test the encryption
# print(encrypt("ID=U79110TS2024PTC187370&requestID=cin"))
# print("DIN", encrypt("10675001"))