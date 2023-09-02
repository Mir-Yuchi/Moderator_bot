from datetime import datetime
from typing import Union, Any

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin
from .tariffs import Tariff


class BotClient(BASE, AsyncBaseModelMixin):
    __tablename__ = 'bot_clients'

    tg_id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(server_default='Пользователь')


class ClientSubscribe(BASE, AsyncBaseModelMixin):
    __tablename__ = 'client_subscribe'
    __table_args__ = (
        sa.UniqueConstraint('client_id', 'tariff_id', 'group_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(sa.BIGINT)
    client_id: Mapped[int] = mapped_column(sa.ForeignKey(
        f'{BotClient.__tablename__}.tg_id'
    ))
    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey(
        f'{Tariff.__tablename__}.id'
    ))
    expire_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    bot_settings: Mapped[dict[Union[str, int], Any]]
    first_time_use: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)

    def expired(self):
        return self.expire_date < datetime.utcnow()
