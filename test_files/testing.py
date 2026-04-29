import os

UPLOAD_DIR = "uploads"


def save_file(filename, content):
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "w") as f:
        f.write(content)

    return path


def read_file(filename):
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "r") as f:
        return f.read()
