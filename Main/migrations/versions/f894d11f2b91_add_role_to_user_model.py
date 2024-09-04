"""Add role to User model

Revision ID: f894d11f2b91
Revises: 
Create Date: 2024-09-04 13:10:17.591460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f894d11f2b91'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'role' column with a default value
    op.add_column('user', sa.Column('role', sa.String(length=10), nullable=False, server_default='user'))


def downgrade():
    # Remove the 'role' column
    op.drop_column('user', 'role')
