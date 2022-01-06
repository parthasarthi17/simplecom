"""empty message

Revision ID: d4217cd434f7
Revises: 7709dfb0356d
Create Date: 2021-12-30 09:57:48.040649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4217cd434f7'
down_revision = '7709dfb0356d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usercart', sa.Column('total', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usercart', 'total')
    # ### end Alembic commands ###