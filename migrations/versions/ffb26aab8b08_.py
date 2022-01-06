"""empty message

Revision ID: ffb26aab8b08
Revises: 6b49758187f0
Create Date: 2021-12-29 10:56:01.350592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffb26aab8b08'
down_revision = '6b49758187f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('speaicaloffer', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'speaicaloffer')
    # ### end Alembic commands ###
