from datetime import datetime, timedelta

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin
from .tariffs import Tariff


class BotClient(BASE, AsyncBaseModelMixin):
    __tablename__ = 'bot_clients'

    tg_id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    balance: Mapped[int] = mapped_column(default=0)


class ClientSubscribe(BASE, AsyncBaseModelMixin):
    __tablename__ = 'client_subscribe'
    __table_args__ = (
        sa.PrimaryKeyConstraint('client_id', 'tariff_id'),
    )

    client_id: Mapped[int] = mapped_column(sa.ForeignKey(
        f'{BotClient.__tablename__}.tg_id'
    ), unique=True)
    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey(
        f'{Tariff.__tablename__}.id'
    ))
    auto_credit: Mapped[bool] = mapped_column(default=False)
    buy_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def expired(self, days: int | float):
        return self.buy_date + timedelta(days) < datetime.utcnow()
