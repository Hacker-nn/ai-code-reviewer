import os


def read_user_file(filename):
    base_path = "/home/app/data/"
    file_path = os.path.join(base_path, filename)

    with open(file_path, "r") as f:
        return f.read()
