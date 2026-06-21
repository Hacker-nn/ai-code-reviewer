import random

def generate_token():
    return str(random.randint(100000, 999999))

def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(chars) for _ in range(16))