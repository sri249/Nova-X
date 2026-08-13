"""add_phase5_fields

Revision ID: 3026_07_30_234000
Revises: 2026_07_30_232413
Create Date: 2026-07-30 23:40:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '3026_07_30_234000'
down_revision: str | None = '2026_07_30_232413'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # 1. Create investor_hub table
    op.create_table(
        'investor_hub',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('executive_summary', sa.String(), nullable=True),
        sa.Column('investment_memo', sa.String(), nullable=True),
        sa.Column('funding_strategy', sa.String(), nullable=True),
        sa.Column('one_page_profile', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('due_diligence_checklist', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('milestone_roadmap', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('pitch_deck', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )

    # 2. Create risk_profile table
    op.create_table(
        'risk_profile',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('technical_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('market_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('financial_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('legal_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('execution_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('hiring_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )

    # 3. Create task_planner table
    op.create_table(
        'task_planner',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('immediate_tasks', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('day_30_plan', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('day_90_plan', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('month_6_plan', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('fundraising_timeline', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('product_timeline', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )

    # 4. Create ai_mentor_analysis table
    op.create_table(
        'ai_mentor_analysis',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('strengths', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('weaknesses', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('missing_information', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('risk_alerts', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('recommended_next_actions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('weekly_priorities', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('ai_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )


def downgrade() -> None:
    op.drop_table('ai_mentor_analysis')
    op.drop_table('task_planner')
    op.drop_table('risk_profile')
    op.drop_table('investor_hub')
