"""Add column tradeable to Card model

Revision ID: 0d3a195f26e0
Revises: 77f898267eaa
Create Date: 2022-08-07 16:12:27.855270

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d3a195f26e0'
down_revision = '77f898267eaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('card', sa.Column('tradeable', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('card', 'tradeable')
    # ### end Alembic commands ###