from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass(frozen=True)
class Miscellaneous:
    BASE_DIR: Path = Path(__file__).parent.parent
    TARIFF_TRIAL_DAYS: int = 5
    STATIC_DIR: Path = BASE_DIR / 'tgbot/static'
    OBSCENE_WORDS_FILE: Path = STATIC_DIR / 'mat.txt'


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


@dataclass(frozen=True)
class RedisDbConfig(DbConfig):
    database: int = 1

    def sync_url(self):
        return f'redis://{self.host}:{self.port}/{self.database}'


@dataclass(frozen=True)
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool
    SUBSCRIBE_PAYMENT_PROVIDER_TOKEN: str
    PAYMENTS_CURRENCY: str = 'RUB'


@dataclass(frozen=True)
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


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


def load_redis_config(path: str | Path = None) -> RedisDbConfig:
    env = Env()
    env.read_env(path)
    return RedisDbConfig(
        env.str('REDIS_HOST'),
        env.str('REDIS_PORT'),
        env.str('REDIS_DB'),
    )


def load_tgbot_config(path: str | Path = None) -> TgBot:
    env = Env()
    env.read_env(path)
    return TgBot(
        token=env.str('BOT_TOKEN'),
        admin_ids=list(map(int, env.str('ADMINS').split(','))),
        use_redis=env.bool('USE_REDIS'),
        SUBSCRIBE_PAYMENT_PROVIDER_TOKEN=env.str(
            'SUBSCRIBE_PAYMENT_PROVIDER_TOKEN'
        ),
        PAYMENTS_CURRENCY=env.str('PAYMENTS_CURRENCY')
    )


def load_config(path: str | Path = None) -> Config:
    return Config(
        tg_bot=load_tgbot_config(path),
        db=load_db_config(path),
        misc=Miscellaneous()
    )
