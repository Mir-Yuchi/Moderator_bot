"""subscribe-buy-date

Revision ID: 4a25c2bac6ad
Revises: 5aa596257452
Create Date: 2023-08-30 20:36:04.355812

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a25c2bac6ad'
down_revision: Union[str, None] = '5aa596257452'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('client_subscribe', sa.Column('buy_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('client_subscribe', 'buy_date')
    # ### end Alembic commands ###