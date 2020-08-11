"""empty message

Revision ID: 45eba2b84418
Revises:
Create Date: 2020-08-09 18:50:40.515516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision = '45eba2b84418'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), default=func.now()),
    sa.Column('updated_at', sa.DateTime(), default=func.now(), onupdate=func.now()),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), default=func.now()),
    sa.Column('updated_at', sa.DateTime(), default=func.now(), onupdate=func.now()),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('user', sa.String(), default="user"),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), default=func.now()),
    sa.Column('updated_at', sa.DateTime(), default=func.now(), onupdate=func.now()),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), default=func.now()),
    sa.Column('updated_at', sa.DateTime(), default=func.now(), onupdate=func.now()),
    sa.Column('total_sum', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('mail', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_to_meal',
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meals.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.Column('created_at', sa.DateTime(), default=func.now()),
    sa.Column('updated_at', sa.DateTime(), default=func.now(), onupdate=func.now()),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_to_meal')
    op.drop_table('orders')
    op.drop_table('meals')
    op.drop_table('users')
    op.drop_table('categories')
    # ### end Alembic commands ###