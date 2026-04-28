import hashlib
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}:{dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, hashed = stored.split(":")
    except ValueError:
        return False

    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return dk.hex() == hashed
