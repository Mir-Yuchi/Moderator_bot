from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass(frozen=True)
class Miscellaneous:
    BASE_DIR: Path = Path(__file__).parent.parent


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    database: str

    def sync_url(self):
        raise NotImplementedError

    def async_url(self):
        raise NotImplementedError


@dataclass(frozen=True)
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


@dataclass(frozen=True)
class PostgresDbConfig(DbConfig):
    user: str
    password: str

    def sync_url(self):
        return (
            f'postgresql+psycopg2://{self.user}:{self.password}@'
            f'{self.host}:{self.port}/{self.database}'
        )

    def async_url(self):
        return (
            f'postgresql+asyncpg://{self.user}:{self.password}@'
            f'{self.host}:{self.port}/{self.database}'
        )


def load_db_config(path: str | Path = None) -> PostgresDbConfig:
    env = Env()
    env.read_env(path)
    return PostgresDbConfig(
        host=env.str('DB_HOST'),
        port=env.str('DB_PORT'),
        password=env.str('DB_PASSWORD'),
        user=env.str('DB_USER'),
        database=env.str('DB_NAME')
    )


def load_tgbot_config(path: str | Path = None) -> TgBot:
    env = Env()
    env.read_env(path)
    return TgBot(
        token=env.str("BOT_TOKEN"),
        admin_ids=list(map(int, env.str("ADMINS").split(","))),
        use_redis=env.bool("USE_REDIS"),
    )


def load_config(path: str | Path = None) -> Config:
    return Config(
        tg_bot=load_tgbot_config(path),
        db=load_db_config(path),
        misc=Miscellaneous()
    )
