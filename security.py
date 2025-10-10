import os, hashlib, binascii

class Security:
    @staticmethod
    def hash_password(password):
        salt = os.urandom(16)                  
        dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 310000, dklen=32)
        return f"{binascii.hexlify(salt).decode()}:{binascii.hexlify(dk).decode()}"
