"""Add trade detail columns to Trade model

Revision ID: 77f898267eaa
Revises: bc1f358481a2
Create Date: 2022-08-07 14:57:46.035918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77f898267eaa'
down_revision = 'bc1f358481a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade', sa.Column('requester_id', sa.Integer(), nullable=False))
    op.add_column('trade', sa.Column('requester_cards', sa.ARRAY(sa.Integer()), nullable=False))
    op.add_column('trade', sa.Column('counterparty_id', sa.Integer(), nullable=False))
    op.add_column('trade', sa.Column('counterparty_cards', sa.ARRAY(sa.Integer()), nullable=False))
    op.create_foreign_key(None, 'trade', 'trader', ['requester_id'], ['id'])
    op.create_foreign_key(None, 'trade', 'trader', ['counterparty_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trade', type_='foreignkey')
    op.drop_constraint(None, 'trade', type_='foreignkey')
    op.drop_column('trade', 'counterparty_cards')
    op.drop_column('trade', 'counterparty_id')
    op.drop_column('trade', 'requester_cards')
    op.drop_column('trade', 'requester_id')
    # ### end Alembic commands ###
