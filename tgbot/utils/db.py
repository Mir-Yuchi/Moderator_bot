from contextlib import contextmanager, asynccontextmanager

from sqlalchemy import create_engine
import sqlalchemy.ext.asyncio as sa_async
from sqlalchemy.orm import sessionmaker


class Singleton(type):
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]


class DbManager(metaclass=Singleton):

    def __init__(self, db_dsn: str = '', echo: bool = True):
        self.engine = create_engine(db_dsn, echo=echo)
        self.session = sessionmaker(self.engine)

    @contextmanager
    def db_session(self):
        try:
            with self.session() as session:
                yield session
        finally:
            session.close()


class AsyncDbManager(metaclass=Singleton):

    def __init__(self, db_dsn: str = '', echo: bool = False):
        self.engine = sa_async.create_async_engine(db_dsn, echo=echo)
        self.session = sa_async.async_sessionmaker(self.engine)

    @asynccontextmanager
    async def db_session(self) -> sa_async.AsyncSession:
        try:
            async with self.session() as session:
                yield session
        finally:
            await session.close()
