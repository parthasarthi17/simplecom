"""empty message

Revision ID: 7709dfb0356d
Revises: e880a09af34c
Create Date: 2021-12-30 09:54:44.221599

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7709dfb0356d'
down_revision = 'e880a09af34c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usercart', 'total')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usercart', sa.Column('total', mysql.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
