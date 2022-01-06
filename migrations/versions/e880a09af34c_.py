"""empty message

Revision ID: e880a09af34c
Revises: 0f36fa6f4607
Create Date: 2021-12-30 09:30:06.880179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e880a09af34c'
down_revision = '0f36fa6f4607'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usercart', sa.Column('total', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usercart', 'total')
    # ### end Alembic commands ###
