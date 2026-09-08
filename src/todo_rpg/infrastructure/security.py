from passlib.hash import argon2
from todo_rpg.infrastructure.config import config
from todo_rpg.application.interfaces import PasswordManagerProtocol


class PasswordManager(PasswordManagerProtocol):
    def __init__(
        self,
        time_cost: int = 1,
        memory_cost: int = 64 * 1024,
        parallelism: int = 2,
        paper: str = config.security.paper.get_secret_value(),
    ):  # paper part will be changed
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.paper = paper

    def hash_password(self, password: str):
        password_hash = argon2.using(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
        ).hash(password + self.paper)
        return password_hash

    def password_verify(self, password: str, password_hash: str):
        return argon2.verify(password + self.paper, password_hash)
