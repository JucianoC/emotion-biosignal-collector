"""create signals table

Revision ID: 12af09d88e82
Revises: 
Create Date: 2019-03-11 21:27:46.844912+00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '12af09d88e82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'signals', sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('id_subject', sa.Integer, nullable=False),
        sa.Column('id_session', sa.Integer, nullable=False),
        sa.Column('id_collect', sa.Integer, nullable=False),
        sa.Column('date_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('ppg_signal', sa.Float, nullable=False),
        sa.Column('eda_signal', sa.Float, nullable=False),
        sa.Column('skt_signal', sa.Float, nullable=False),
        sa.Column('sam_arousal', sa.Float, nullable=False),
        sa.Column('sam_valence', sa.Float, nullable=False),
        sa.Column('id_iaps', sa.String(10), nullable=False))


def downgrade():
    op.drop_table('signals')
