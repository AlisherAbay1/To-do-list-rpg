from passlib.hash import argon2
from todo_rpg.infrastructure.config import config


def hash_password(password: str):
    paper = config.security.paper.get_secret_value()
    password_hash = argon2.using(
        time_cost=1, memory_cost=64 * 1024, parallelism=2
    ).hash(password + paper)
    return password_hash


def password_verify(password: str, password_hash: str):
    paper = config.security.paper.get_secret_value()
    return argon2.verify(password + paper, password_hash)
