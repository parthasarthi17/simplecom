"""empty message

Revision ID: 0f36fa6f4607
Revises: ffb26aab8b08
Create Date: 2021-12-29 12:24:22.102957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f36fa6f4607'
down_revision = 'ffb26aab8b08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('no_ratings', sa.Integer(), nullable=True))
    op.add_column('product', sa.Column('avg_rating', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'avg_rating')
    op.drop_column('product', 'no_ratings')
    # ### end Alembic commands ###
