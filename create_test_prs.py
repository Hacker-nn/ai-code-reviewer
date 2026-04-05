import subprocess
import os

BUGS = {
    "pr01_hardcoded_password.py": """
def connect_db():
    password = "admin123"
    username = "root"
    return f"mysql://{{username}}:{{password}}@localhost/db"
""",
    "pr02_sql_injection.py": """
import sqlite3

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()
""",
    "pr03_divide_by_zero.py": """
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)
""",
    "pr04_no_input_validation.py": """
def create_user(age, email):
    user = {"age": int(age), "email": email}
    return user
""",
    "pr05_infinite_loop.py": """
def find_item(items, target):
    i = 0
    while True:
        if items[i] == target:
            return i
        i += 1
""",
    "pr06_unused_imports.py": """
import os
import sys
import json
import random
import hashlib

def greet(name):
    return f"Hello, {{name}}"
""",
    "pr07_mutable_default.py": """
def add_item(item, items=[]):
    items.append(item)
    return items
""",
    "pr08_swallowed_exception.py": """
def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        pass
""",
    "pr09_hardcoded_secrets.py": """
API_KEY = "sk-abc123secretkey"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def call_api():
    return API_KEY
""",
    "pr10_no_error_handling.py": """
import requests

def fetch_data(url):
    response = requests.get(url)
    return response.json()
""",
    "pr11_xss_vulnerability.py": """
from flask import request

def render_comment():
    user_input = request.args.get("comment")
    return f"<div>{{user_input}}</div>"
""",
    "pr12_insecure_random.py": """
import random

def generate_token():
    return str(random.randint(100000, 999999))

def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(chars) for _ in range(16))
""",
    "pr13_memory_leak.py": """
cache = {}

def process_request(request_id, data):
    result = data * 2
    cache[request_id] = result
    return result
""",
    "pr14_race_condition.py": """
import threading

counter = 0

def increment():
    global counter
    temp = counter
    temp += 1
    counter = temp

threads = [threading.Thread(target=increment) for _ in range(100)]
for t in threads:
    t.start()
""",
    "pr15_plaintext_password.py": """
import sqlite3

def save_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users VALUES (?, ?)",
        (username, password)
    )
    conn.commit()
""",
    "pr16_good_code.py": """
import hashlib
import secrets

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{{salt}}:{{hashed}}"

def verify_password(password: str, stored: str) -> bool:
    salt, hashed = stored.split(":")
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed
""",
    "pr17_good_code_2.py": """
from typing import Optional

def find_user(users: list[dict], user_id: int) -> Optional[dict]:
    return next((u for u in users if u["id"] == user_id), None)

def paginate(items: list, page: int, page_size: int = 10) -> list:
    if page < 1 or page_size < 1:
        raise ValueError("page and page_size must be positive")
    start = (page - 1) * page_size
    return items[start:start + page_size]
""",
    "pr18_global_variable_abuse.py": """
total_price = 0
discount = 0
tax = 0

def set_price(price):
    global total_price
    total_price = price

def apply_discount(d):
    global discount, total_price
    discount = d
    total_price = total_price - discount

def apply_tax(t):
    global tax, total_price
    tax = t
    total_price = total_price + tax
""",
    "pr19_type_confusion.py": """
def add(a, b):
    return a + b

result1 = add(1, 2)
result2 = add("1", "2")
result3 = add([1], [2])
result4 = add(1, "2")
""",
    "pr20_debug_code.py": """
def process_payment(amount, card_number):
    print(f"DEBUG: Processing payment of {{amount}}")
    print(f"DEBUG: Card number is {{card_number}}")
    import pdb; pdb.set_trace()
    return True
""",
}


def run(cmd, check=True):
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"  ERROR: {result.stderr}")
        raise SystemExit(1)
    return result


def create_test_prs():
    os.makedirs("test_files", exist_ok=True)

    for filename, code in BUGS.items():
        branch = filename.replace(".py", "").replace("_", "-")[:20]
        branch = f"test/{branch}"

        print(f"\nCreating PR for: {filename}")

        # checkout main and pull latest
        run("git checkout main")
        run("git pull origin main --rebase", check=False)

        # create fresh branch
        run(f"git checkout -b {branch}")

        # write the file
        filepath = f"test_files/{filename}"
        with open(filepath, "w") as f:
            f.write(code.strip())

        # commit and push
        run(f"git add {filepath}")
        run(f'git commit -m "test: add {filename}"')
        run(f"git push origin {branch} --force")

        # create PR via GitHub CLI
        pr_title = filename.replace(".py", "").replace("_", " ").title()
        run(
            f'gh pr create --title "{pr_title}" --body "Automated test PR" --base main --head {branch}'
        )

        print(f"  PR created for {filename}")


if __name__ == "__main__":
    print("Starting test PR creation...")
    print("Make sure you have GitHub CLI (gh) installed and authenticated.\n")
    create_test_prs()
    print("\nAll test PRs created!")
