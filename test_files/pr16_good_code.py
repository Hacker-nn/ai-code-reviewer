import hashlib
import secrets

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{{salt}}:{{hashed}}"

def verify_password(password: str, stored: str) -> bool:
    salt, hashed = stored.split(":")
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed