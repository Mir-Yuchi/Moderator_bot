from typing import Union, Any

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from . import BASE, AsyncBaseModelMixin


class AdminGroupBot(BASE, AsyncBaseModelMixin):

    __tablename__ = 'admin_group_bots'

    group_id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True)
    admin_id: Mapped[int] = mapped_column(sa.BIGINT)
    bot_settings: Mapped[dict[Union[str, int], Any]]
