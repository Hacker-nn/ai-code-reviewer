def connect_db():
    password = "admin123"
    username = "root"
    return f"mysql://{{username}}:{{password}}@localhost/db"