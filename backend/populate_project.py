import asyncio
import logging
import uuid

from app.features.startup_health.models import StartupHealth
from sqlalchemy.future import select

from app.core.database import async_session_maker
from app.features.financial_planner.models import FinancialPlanner
from app.features.innovation_dna.models import InnovationDNA
from app.features.market_intelligence.models import MarketIntelligence
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.projects.models import Project
from app.features.startup_formation.models import StartupFormation
from app.services.ai import ai_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def populate_project():
    project_id = uuid.UUID('7aad881f-a0ba-46d3-8cd9-ae1a51c17062')
    
    async with async_session_maker() as db:
        proj_result = await db.execute(select(Project).where(Project.id == project_id))
        project = proj_result.scalars().first()
        if not project:
            logger.error(f"Project {project_id} not found!")
            return

        logger.info(f"Populating project: {project.name}")

        # 1. Problem Discovery
        pa_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
        pa = pa_result.scalars().first()
        if not pa:
            logger.info("Generating Problem Discovery...")
            ai_out = await ai_service.generate_problem_discovery({
                "title": project.name,
                "description": project.description,
                "industry": "Tech",
                "country": "USA",
                "target_users": "Everyone",
                "existing_solutions": "None",
                "pain_points": "Many"
            })
            pa = ProblemAnalysis(
                project_id=project_id,
                core_problem=ai_out.problem_summary,
                problem_summary=ai_out.problem_summary,
                root_cause_analysis=ai_out.root_cause_analysis,
                stakeholders=ai_out.stakeholders,
                impact_analysis=ai_out.impact_analysis,
                opportunity_score=ai_out.opportunity_score,
                sdg_alignment=ai_out.sdg_alignment,
                key_insights=ai_out.key_insights
            )
            db.add(pa)
            await db.commit()

        # 2. Innovation DNA
        dna_result = await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))
        dna = dna_result.scalars().first()
        if not dna:
            logger.info("Generating Innovation DNA...")
            ai_out = await ai_service.generate_innovation_dna({
                "problem_summary": pa.problem_summary,
                "target_audience": pa.stakeholders,
                "innovation_focus": "Tech"
            })
            dna = InnovationDNA(
                project_id=project_id,
                value_proposition=ai_out.value_proposition,
                core_innovation=ai_out.core_innovation,
                unique_differentiators=ai_out.unique_differentiators,
                business_model_canvas=ai_out.business_model_canvas,
                moat_analysis=ai_out.moat_analysis,
                pivot_scenarios=ai_out.pivot_scenarios,
                ai_metadata=ai_out.ai_metadata
            )
            db.add(dna)
            await db.commit()

        # 3. Startup Formation
        sf_result = await db.execute(select(StartupFormation).where(StartupFormation.project_id == project_id))
        sf = sf_result.scalars().first()
        if not sf:
            logger.info("Generating Startup Formation...")
            ai_out = await ai_service.generate_startup_formation({
                "value_proposition": dna.value_proposition,
                "business_model_canvas": dna.business_model_canvas
            })
            sf = StartupFormation(
                project_id=project_id,
                startup_name=ai_out.startup_name,
                tagline=ai_out.tagline,
                mission_statement=ai_out.mission_statement,
                vision_statement=ai_out.vision_statement,
                core_values=ai_out.core_values,
                brand_personality=ai_out.brand_personality,
                target_audience_persona=ai_out.target_audience_persona,
                elevator_pitch=ai_out.elevator_pitch,
                ai_metadata=ai_out.ai_metadata
            )
            db.add(sf)
            await db.commit()

        # 4. Market Intelligence
        mi_result = await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))
        mi = mi_result.scalars().first()
        if not mi:
            logger.info("Generating Market Intelligence...")
            ai_out = await ai_service.generate_market_intelligence({
                "startup_name": sf.startup_name,
                "industry": "Tech",
                "value_proposition": dna.value_proposition
            })
            mi = MarketIntelligence(
                project_id=project_id,
                tam_sam_som=ai_out.tam_sam_som,
                competitor_matrix=ai_out.competitor_matrix,
                swot_analysis=ai_out.swot_analysis,
                market_trends=ai_out.market_trends,
                regulatory_landscape=ai_out.regulatory_landscape,
                go_to_market_strategy=ai_out.go_to_market_strategy,
                ai_metadata=ai_out.ai_metadata
            )
            db.add(mi)
            await db.commit()

        # 5. Financial Planner
        fp_result = await db.execute(select(FinancialPlanner).where(FinancialPlanner.project_id == project_id))
        fp = fp_result.scalars().first()
        if not fp:
            logger.info("Generating Financial Planner...")
            ai_out = await ai_service.generate_financial_planner({
                "startup_name": sf.startup_name,
                "business_model": "SaaS"
            })
            fp = FinancialPlanner(
                project_id=project_id,
                revenue_model=ai_out.revenue_model,
                pricing_strategy=ai_out.pricing_strategy,
                cost_structure=ai_out.cost_structure,
                financial_projections=ai_out.financial_projections,
                funding_requirements=ai_out.funding_requirements,
                key_metrics=ai_out.key_metrics,
                break_even_analysis=ai_out.break_even_analysis,
                ai_metadata=ai_out.ai_metadata
            )
            db.add(fp)
            await db.commit()

        # 6. Startup Health
        sh_result = await db.execute(select(StartupHealth).where(StartupHealth.project_id == project_id))
        sh = sh_result.scalars().first()
        if not sh:
            logger.info("Generating Startup Health...")
            ai_out = await ai_service.generate_startup_health({
                "startup_name": sf.startup_name
            })
            sh = StartupHealth(
                project_id=project_id,
                overall_score=ai_out.overall_score,
                health_metrics=ai_out.health_metrics,
                risk_factors=ai_out.risk_factors,
                recommendations=ai_out.recommendations,
                milestones=ai_out.milestones,
                ai_metadata=ai_out.ai_metadata
            )
            db.add(sh)
            await db.commit()

        logger.info("Project successfully populated with AI data!")

if __name__ == "__main__":
    asyncio.run(populate_project())
