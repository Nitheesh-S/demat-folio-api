from cryptography.fernet import Fernet
from django.conf import settings


def generate_key():
    """
    Generates a new Fernet key.
    """
    return Fernet.generate_key()


def encrypt_message(message, key=settings.FERNET_KEY):
    """
    Encrypts a message using the provided key.
    Returns the encrypted message as string.
    """
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()


def decrypt_message(encrypted_message, key=settings.FERNET_KEY):
    """
    Decrypts an encrypted message using the provided key.
    Returns the decrypted message as a string.
    """
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()
    return decrypted_message