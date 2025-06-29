# auth_system.py

import hashlib
import os

USERS_FILE = "users.txt"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            f.write(f"admin,{hash_password('password')}\n")
            f.write(f"user,{hash_password('1234')}\n")

def register(username, password):
    initialize_users()
    with open(USERS_FILE, 'r') as f:
        for line in f:
            if line.split(',')[0].strip() == username:
                return "User already exists."
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username},{hash_password(password)}\n")
    return "User registered successfully."

def login(username, password):
    initialize_users()
    hashed = hash_password(password)
    with open(USERS_FILE, 'r') as f:
        for line in f:
            user, pw = line.strip().split(',')
            if user.strip() == username and pw.strip() == hashed:
                return True
    return False
