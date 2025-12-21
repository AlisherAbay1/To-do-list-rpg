from passlib.hash import argon2
from dotenv import dotenv_values 

def hash_password(password: str):
    paper = dotenv_values(".env")["PAPER"]
    if not paper:
        paper = ''
    password_hash = argon2.using(time_cost=1, memory_cost=64*1024, parallelism=2).hash(password + paper)
    return password_hash

def password_verify(password: str, password_hash: str):
    paper = dotenv_values(".env")["PAPER"]
    if not paper:
        paper = ''
    return argon2.verify(password + paper, password_hash)