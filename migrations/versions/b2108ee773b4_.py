"""empty message

Revision ID: b2108ee773b4
Revises: e750731367cf
Create Date: 2020-02-21 01:56:58.410081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2108ee773b4'
down_revision = 'e750731367cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('comment', sa.Text(), nullable=False))
    op.add_column('orders', sa.Column('order', sa.Text(), nullable=False))
    op.add_column('orders', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.drop_constraint('orders_order_id_fkey', 'orders', type_='foreignkey')
    op.create_foreign_key(None, 'orders', 'users', ['owner_id'], ['id'])
    op.drop_column('orders', 'comments')
    op.drop_column('orders', 'order_id')
    op.drop_column('orders', 'orders')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('orders', sa.TEXT(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('comments', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.create_foreign_key('orders_order_id_fkey', 'orders', 'users', ['order_id'], ['id'])
    op.drop_column('orders', 'owner_id')
    op.drop_column('orders', 'order')
    op.drop_column('orders', 'comment')
    # ### end Alembic commands ###
