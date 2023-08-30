import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin
from .features import Features


class Tariff(BASE, AsyncBaseModelMixin):
    __tablename__ = 'tariffs'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    sum: Mapped[int]
    limitation_days: Mapped[int]
    groups_count: Mapped[int]


class TariffFeature(BASE, AsyncBaseModelMixin):
    __tablename__ = 'tariff_features'
    __table_args__ = (
        sa.PrimaryKeyConstraint('tariff_id', 'feature_id'),
    )

    tariff_id: Mapped[int] = mapped_column(sa.ForeignKey(
        f'{Tariff.__tablename__}.id'
    ))
    feature_id: Mapped[int] = mapped_column(sa.ForeignKey(
        f'{Features.__tablename__}.id'
    ))
