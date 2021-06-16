"""create user table

Revision ID: 6f95504a7163
Revises: 
Create Date: 2021-06-11 02:52:14.438122

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6f95504a7163'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('auth0_id', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('user')
