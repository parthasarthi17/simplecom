"""empty message

Revision ID: 832fa635aa33
Revises: d4217cd434f7
Create Date: 2022-01-02 17:32:37.490397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '832fa635aa33'
down_revision = 'd4217cd434f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usercart', sa.Column('status', sa.String(length=40), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usercart', 'status')
    # ### end Alembic commands ###
