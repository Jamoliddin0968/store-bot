"""empty message

Revision ID: e2934b440145
Revises: 0c0186e5116a
Create Date: 2024-05-24 17:13:07.788081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_file
import fastapi_storages


# revision identifiers, used by Alembic.
revision: str = 'e2934b440145'
down_revision: Union[str, None] = '0c0186e5116a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('words',
    sa.Column('value', sa.String(length=255), nullable=True),
    sa.Column('value_uz', sa.String(length=255), nullable=True),
    sa.Column('value_ru', sa.String(length=255), nullable=True),
    sa.Column('value_en', sa.String(length=255), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('value')
    )
    op.drop_table('tarjimalar')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tarjimalar',
    sa.Column('object_type', sa.VARCHAR(length=255), nullable=True),
    sa.Column('object_id', sa.INTEGER(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('words')
    # ### end Alembic commands ###
