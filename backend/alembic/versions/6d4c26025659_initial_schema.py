"""initial_schema

Revision ID: 6d4c26025659
Revises: 
Create Date: 2026-09-27 10:24:25.607176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6d4c26025659'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create Enums
    station_status = postgresql.ENUM('healthy', 'warning', 'faulty', name='stationstatus')
    station_status.create(op.get_bind(), checkfirst=True)
    
    reading_source = postgresql.ENUM('physical_sensor', 'weather_api', name='readingsource')
    reading_source.create(op.get_bind(), checkfirst=True)
    
    fault_type = postgresql.ENUM('Spike', 'Frozen', 'Drift', 'CommFailure', 'MissingData', name='faulttype')
    fault_type.create(op.get_bind(), checkfirst=True)
    
    anomaly_status = postgresql.ENUM('critical', 'warning', 'genuine_event', 'resolved', name='anomalystatus')
    anomaly_status.create(op.get_bind(), checkfirst=True)
    
    operator_decision = postgresql.ENUM('pending', 'accepted', 'rejected', 'manual_review', name='operatordecision')
    operator_decision.create(op.get_bind(), checkfirst=True)
    
    fault_action = postgresql.ENUM('replaced', 'calibrated', 'reset', 'pending', 'scheduled', name='faultaction')
    fault_action.create(op.get_bind(), checkfirst=True)

    # 2. Create tables
    op.create_table(
        'stations',
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('location_name', sa.String(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('active_since', sa.Date(), nullable=True),
        sa.Column('status', station_status, nullable=True),
        sa.PrimaryKeyConstraint('station_id')
    )

    op.create_table(
        'readings',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Float(), nullable=True),
        sa.Column('pressure', sa.Float(), nullable=True),
        sa.Column('source', reading_source, nullable=True),
        sa.ForeignKeyConstraint(['station_id'], ['stations.station_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # TimescaleDB hypertable for readings
    # removed

    op.create_table(
        'anomalies',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('reading_id', sa.Integer(), nullable=False),
        sa.Column('reading_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('detected_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('anomaly_score', sa.Float(), nullable=True),
        sa.Column('fault_type', fault_type, nullable=True),
        sa.Column('status', anomaly_status, nullable=True),
        sa.Column('temporal_evidence', sa.JSON(), nullable=False),
        sa.Column('physical_consistency', sa.JSON(), nullable=False),
        sa.Column('spatial_evidence', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['station_id'], ['stations.station_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reading_id', 'reading_timestamp'], ['readings.id', 'readings.timestamp'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'corrections',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('anomaly_id', sa.Integer(), nullable=False),
        sa.Column('original_value', sa.Float(), nullable=True),
        sa.Column('corrected_value', sa.Float(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('methodology', sa.JSON(), nullable=True),
        sa.Column('operator_decision', operator_decision, nullable=True),
        sa.ForeignKeyConstraint(['anomaly_id'], ['anomalies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'sensor_health',
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('fleet_health_score', sa.Float(), nullable=True),
        sa.Column('mtbf_days', sa.Integer(), nullable=True),
        sa.Column('last_calculated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('degradation_trend', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['station_id'], ['stations.station_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('station_id')
    )

    op.create_table(
        'fault_history',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('station_id', sa.String(), nullable=False),
        sa.Column('component', sa.String(), nullable=True),
        sa.Column('action', fault_action, nullable=True),
        sa.Column('event_date', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['station_id'], ['stations.station_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('fault_history')
    op.drop_table('sensor_health')
    op.drop_table('corrections')
    op.drop_table('anomalies')
    op.drop_table('readings')
    op.drop_table('stations')
    
    op.execute("DROP TYPE IF EXISTS faultaction")
    op.execute("DROP TYPE IF EXISTS operatordecision")
    op.execute("DROP TYPE IF EXISTS anomalystatus")
    op.execute("DROP TYPE IF EXISTS faulttype")
    op.execute("DROP TYPE IF EXISTS readingsource")
    op.execute("DROP TYPE IF EXISTS stationstatus")
