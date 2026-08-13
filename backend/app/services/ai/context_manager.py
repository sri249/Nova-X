import json


class ContextManager:
    @staticmethod
    def build_problem_context(problem_data: dict) -> str:
        return json.dumps(problem_data, indent=2)

    @staticmethod
    def build_innovation_context(innovation_data: dict) -> str:
        return json.dumps(innovation_data, indent=2)

    @staticmethod
    def build_full_context(problem_data: dict, innovation_data: dict, startup_data: dict | None = None) -> str:
        context = {
            "problem": problem_data,
            "innovation": innovation_data
        }
        if startup_data:
            context["startup"] = startup_data
        return json.dumps(context, indent=2)

    @staticmethod
    async def build_full_project_context(project_id, db) -> str:
        from sqlalchemy import select

        from app.features.financial_planner.models import FinancialPlan
        from app.features.innovation_dna.models import InnovationDNA
        from app.features.market_intelligence.models import MarketIntelligence
        from app.features.problem_discovery.models import ProblemAnalysis
        from app.features.startup_formation.models import StartupProfile
        
        context = {}
        
        # Problem
        pa = (await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))).scalars().first()
        if pa: context["problem"] = pa.problem_summary
        
        # DNA
        dna = (await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))).scalars().first()
        if dna: context["innovation"] = dna.unique_value_proposition
        
        # Startup Formation
        sp = (await db.execute(select(StartupProfile).where(StartupProfile.project_id == project_id))).scalars().first()
        if sp: context["startup"] = sp.elevator_pitch
        
        # Market
        mi = (await db.execute(select(MarketIntelligence).where(MarketIntelligence.project_id == project_id))).scalars().first()
        if mi: context["market"] = mi.market_gap_analysis
        
        # Financial
        fp = (await db.execute(select(FinancialPlan).where(FinancialPlan.project_id == project_id))).scalars().first()
        if fp: context["financial"] = fp.runway
        
        return json.dumps(context, indent=2)
