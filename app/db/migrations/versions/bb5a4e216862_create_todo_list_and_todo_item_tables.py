"""create_todo_list_and_todo_item_tables

Revision ID: bb5a4e216862
Revises: 6f95504a7163
Create Date: 2021-06-14 04:26:32.679010

"""
from alembic import op
from sqlalchemy import Column, String, PrimaryKeyConstraint, Integer, Boolean

# revision identifiers, used by Alembic.
revision = 'bb5a4e216862'
down_revision = '6f95504a7163'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'todo_list',
        Column('id', Integer(), nullable=False),
        Column('user_id', String(), nullable=False),
        Column('name', String(), nullable=False),
        PrimaryKeyConstraint('id'))

    op.create_table(
        'todo_item',
        Column('id', Integer(), nullable=False),
        Column('todo_list_id', Integer(), nullable=False),
        Column('name', String(), nullable=False),
        Column('is_complete', Boolean(), nullable=False),
        PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('todo_item')
    op.drop_table('todo_list')
