from passlib.hash import argon2
from todo_rpg.infrastructure.config import Config
from todo_rpg.application.interfaces import PasswordManagerProtocol


class PasswordManager(PasswordManagerProtocol):
    def __init__(self, config: Config):
        self.time_cost = config.security.time_cost
        self.memory_cost = config.security.memory_cost
        self.parallelism = config.security.parallelism
        self.paper = config.security.paper.get_secret_value()

    def hash_password(self, password: str):
        password_hash = argon2.using(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
        ).hash(password + self.paper)
        return password_hash

    def password_verify(self, password: str, password_hash: str):
        return argon2.verify(password + self.paper, password_hash)
