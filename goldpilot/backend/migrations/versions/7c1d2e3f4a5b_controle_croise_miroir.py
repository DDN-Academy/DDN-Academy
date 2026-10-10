"""contrôle croisé TradingView : verdict des signaux miroir

Revision ID: 7c1d2e3f4a5b
Revises: 26ebde2c15bc
Create Date: 2026-10-10 09:00:00
"""
from alembic import op
import sqlalchemy as sa
import goldpilot.db


revision = '7c1d2e3f4a5b'
down_revision = '26ebde2c15bc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('mirror_signals') as b:
        b.add_column(sa.Column('verdict', sa.String(length=40), nullable=True))
        b.add_column(sa.Column('checked_at', goldpilot.db.UTC(timezone=True), nullable=True))


def downgrade():
    with op.batch_alter_table('mirror_signals') as b:
        b.drop_column('checked_at')
        b.drop_column('verdict')
