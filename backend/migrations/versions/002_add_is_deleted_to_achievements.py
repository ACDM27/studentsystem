"""Add is_deleted field to biz_achievements table

Revision ID: 002
Revises: 001
Create Date: 2026-02-12

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    """Add is_deleted column for soft delete functionality"""
    op.add_column('biz_achievements', 
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='0')
    )
    op.create_index(op.f('ix_biz_achievements_is_deleted'), 'biz_achievements', ['is_deleted'])


def downgrade():
    """Remove is_deleted column"""
    op.drop_index(op.f('ix_biz_achievements_is_deleted'), table_name='biz_achievements')
    op.drop_column('biz_achievements', 'is_deleted')
