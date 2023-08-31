from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin


class Features(BASE, AsyncBaseModelMixin):
    __tablename__ = 'features'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
