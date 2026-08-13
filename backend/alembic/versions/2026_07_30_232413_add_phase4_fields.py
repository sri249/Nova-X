"""add phase4 fields

Revision ID: 2026_07_30_232413
Revises: 1a2b3c4d5e6f
Create Date: 2026-07-30 23:24:13.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '2026_07_30_232413'
down_revision = '1a2b3c4d5e6f'
branch_labels = None
depends_on = None

def upgrade():
    # drop old market_analysis table
    op.drop_table('market_analysis')

    # create market_intelligence
    op.create_table('market_intelligence',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('tam_sam_som', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('industry_growth_rate', sa.String(), nullable=True),
        sa.Column('cagr', sa.String(), nullable=True),
        sa.Column('market_maturity', sa.String(), nullable=True),
        sa.Column('customer_personas', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('adoption_curve', sa.String(), nullable=True),
        sa.Column('seasonal_trends', sa.String(), nullable=True),
        sa.Column('market_trends', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('geographic_expansion', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('regulatory_risks', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('emerging_technologies', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('swot_analysis', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('competitor_matrix', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('market_gap_analysis', sa.Text(), nullable=True),
        sa.Column('barriers_to_entry', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('market_readiness_score', sa.Integer(), nullable=True),
        sa.Column('ai_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )

    # create financial_plans
    op.create_table('financial_plans',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('startup_costs', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('monthly_operating_costs', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('hiring_costs', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('marketing_budget', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('infrastructure_cost', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('revenue_forecast', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('cash_flow', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('burn_rate', sa.String(), nullable=True),
        sa.Column('runway', sa.String(), nullable=True),
        sa.Column('break_even_month', sa.String(), nullable=True),
        sa.Column('funding_requirement', sa.String(), nullable=True),
        sa.Column('funding_recommendation', sa.Text(), nullable=True),
        sa.Column('roi_projection', sa.String(), nullable=True),
        sa.Column('ai_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )

    # startup_scores additions
    op.add_column('startup_scores', sa.Column('execution_score', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('startup_scores', sa.Column('financial_score', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('startup_scores', sa.Column('investment_readiness', sa.Integer(), nullable=True, server_default='0'))
    op.add_column('startup_scores', sa.Column('ai_recommendations', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'))

    # projects additions
    op.add_column('projects', sa.Column('project_timeline', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))


def downgrade():
    # projects
    op.drop_column('projects', 'project_timeline')

    # startup_scores
    op.drop_column('startup_scores', 'ai_recommendations')
    op.drop_column('startup_scores', 'investment_readiness')
    op.drop_column('startup_scores', 'financial_score')
    op.drop_column('startup_scores', 'execution_score')

    # financial_plans
    op.drop_table('financial_plans')

    # market_intelligence
    op.drop_table('market_intelligence')

    # recreate market_analysis
    op.create_table('market_analysis',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('tam_sam_som', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('competitors', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'),
        sa.Column('swot_analysis', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )
