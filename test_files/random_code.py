import hashlib

users = {
    "admin": "5f4dcc3b5aa765d61d8327deb882cf99"  # md5("password")
}

def login(username, password):
    hashed = hashlib.md5(password.encode()).hexdigest()

    if username in users:
        if users[username] == hashed:
            return True
    return False

def get_user_data(username):
    return users[username]