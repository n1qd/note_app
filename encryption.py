from cryptography.fernet import Fernet
from private import encryption_key

cipher_suite = Fernet(encryption_key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()



