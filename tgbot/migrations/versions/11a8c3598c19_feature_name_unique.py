"""feature-name-unique

Revision ID: 11a8c3598c19
Revises: 54cbef35603d
Create Date: 2023-08-29 16:11:08.074480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11a8c3598c19'
down_revision: Union[str, None] = '54cbef35603d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(op.f('uq_features_name'), 'features', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_features_name'), 'features', type_='unique')
    # ### end Alembic commands ###