"""add phase3 fields

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2026-07-30 17:00:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # projects
    op.add_column('projects', sa.Column('completion_percentage', sa.Integer(), nullable=True, server_default='0'))
    
    # problem_analysis
    op.add_column('problem_analysis', sa.Column('problem_summary', sa.Text(), nullable=True))
    op.add_column('problem_analysis', sa.Column('stakeholders', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))
    op.add_column('problem_analysis', sa.Column('impact_analysis', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'))
    op.add_column('problem_analysis', sa.Column('opportunity_score', sa.Integer(), nullable=True))
    op.add_column('problem_analysis', sa.Column('sdg_alignment', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))
    op.add_column('problem_analysis', sa.Column('key_insights', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))

    # innovation_dna
    op.add_column('innovation_dna', sa.Column('innovation_score', sa.Integer(), nullable=True))
    op.add_column('innovation_dna', sa.Column('originality_score', sa.Integer(), nullable=True))
    op.add_column('innovation_dna', sa.Column('competitor_overview', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))
    op.add_column('innovation_dna', sa.Column('market_gap', sa.Text(), nullable=True))
    op.add_column('innovation_dna', sa.Column('novelty_analysis', sa.Text(), nullable=True))
    op.add_column('innovation_dna', sa.Column('differentiation', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))
    op.add_column('innovation_dna', sa.Column('patent_potential_indicator', sa.String(), nullable=True))
    op.add_column('innovation_dna', sa.Column('innovation_radar_visualization', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'))

    # startup_profiles
    op.add_column('startup_profiles', sa.Column('tagline', sa.String(), nullable=True))
    op.add_column('startup_profiles', sa.Column('brand_personality', sa.String(), nullable=True))
    op.add_column('startup_profiles', sa.Column('logo_prompt', sa.Text(), nullable=True))
    op.add_column('startup_profiles', sa.Column('color_palette', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))
    op.add_column('startup_profiles', sa.Column('value_proposition', sa.Text(), nullable=True))
    op.add_column('startup_profiles', sa.Column('unique_selling_proposition', sa.Text(), nullable=True))
    op.add_column('startup_profiles', sa.Column('elevator_pitch', sa.Text(), nullable=True))
    op.add_column('startup_profiles', sa.Column('product_roadmap', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))
    op.add_column('startup_profiles', sa.Column('launch_checklist', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='[]'))

    # business_models
    op.add_column('business_models', sa.Column('business_model_canvas', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'))
    op.add_column('business_models', sa.Column('revenue_model', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'))

    # Create StartupScore table
    op.create_table('startup_scores',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('innovation_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('business_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('market_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('technology_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('scalability_score', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('overall_score', sa.Integer(), nullable=True, server_default='0'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('project_id')
    )
    
    # Create AIVersionHistory table
    op.create_table('ai_version_history',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('project_id', sa.UUID(), nullable=False),
        sa.Column('module', sa.String(), nullable=False),
        sa.Column('field_name', sa.String(), nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # drop ai_version_history table
    op.drop_table('ai_version_history')
    
    # drop startup_scores table
    op.drop_table('startup_scores')

    # business_models
    op.drop_column('business_models', 'revenue_model')
    op.drop_column('business_models', 'business_model_canvas')

    # startup_profiles
    op.drop_column('startup_profiles', 'launch_checklist')
    op.drop_column('startup_profiles', 'product_roadmap')
    op.drop_column('startup_profiles', 'elevator_pitch')
    op.drop_column('startup_profiles', 'unique_selling_proposition')
    op.drop_column('startup_profiles', 'value_proposition')
    op.drop_column('startup_profiles', 'color_palette')
    op.drop_column('startup_profiles', 'logo_prompt')
    op.drop_column('startup_profiles', 'brand_personality')
    op.drop_column('startup_profiles', 'tagline')

    # innovation_dna
    op.drop_column('innovation_dna', 'innovation_radar_visualization')
    op.drop_column('innovation_dna', 'patent_potential_indicator')
    op.drop_column('innovation_dna', 'differentiation')
    op.drop_column('innovation_dna', 'novelty_analysis')
    op.drop_column('innovation_dna', 'market_gap')
    op.drop_column('innovation_dna', 'competitor_overview')
    op.drop_column('innovation_dna', 'originality_score')
    op.drop_column('innovation_dna', 'innovation_score')

    # problem_analysis
    op.drop_column('problem_analysis', 'key_insights')
    op.drop_column('problem_analysis', 'sdg_alignment')
    op.drop_column('problem_analysis', 'opportunity_score')
    op.drop_column('problem_analysis', 'impact_analysis')
    op.drop_column('problem_analysis', 'stakeholders')
    op.drop_column('problem_analysis', 'problem_summary')

    # projects
    op.drop_column('projects', 'completion_percentage')
