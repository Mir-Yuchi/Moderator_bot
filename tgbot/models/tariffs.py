from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin


class Tariff(BASE, AsyncBaseModelMixin):
    __tablename__ = 'tariffs'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    sum: Mapped[int]
    limitation_days: Mapped[int]
