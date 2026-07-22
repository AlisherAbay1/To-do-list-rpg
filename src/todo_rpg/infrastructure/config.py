from dataclasses import dataclass
from pathlib import Path
from dature import load, Toml10Source, EnvFileSource, F, EnvSource
from dature.fields.secret_str import SecretStr
from sqlalchemy.engine import URL

_ENV_FILE = Path(__file__).parents[3] / ".env"
_TOML_FILE = Path(__file__).parents[3] / "config.toml"


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    username: str
    password: SecretStr

    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


@dataclass
class RedisConfig:
    host: str
    port: int
    max_age: int
    encoding: str


@dataclass
class FastapiConfig:
    is_production: bool


@dataclass
class SecurityConfig:
    paper: SecretStr


@dataclass
class Config:
    database: DatabaseConfig
    redis: RedisConfig
    fastapi: FastapiConfig
    security: SecurityConfig


def load_config():
    database = load(
        EnvFileSource(
            file=_ENV_FILE,
            field_mapping={F[DatabaseConfig].password: "DB_PASSWORD"},
            skip_if_missing=True,
        ),
        EnvSource(field_mapping={F[DatabaseConfig].password: "DB_PASSWORD"}),
        Toml10Source(file=_TOML_FILE, prefix="database"),
        schema=DatabaseConfig,
    )
    redis = load(Toml10Source(file=_TOML_FILE, prefix="redis"), schema=RedisConfig)
    fastapi = load(
        Toml10Source(file=_TOML_FILE, prefix="fastapi"), schema=FastapiConfig
    )
    security = load(
        EnvFileSource(
            file=_ENV_FILE,
            field_mapping={F[SecurityConfig].paper: "PAPER"},
            skip_if_missing=True,
        ),
        EnvSource(field_mapping={F[SecurityConfig].paper: "PAPER"}),
        schema=SecurityConfig,
    )
    config = Config(database=database, redis=redis, fastapi=fastapi, security=security)
    return config


config = load_config()
