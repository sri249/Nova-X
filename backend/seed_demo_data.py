import asyncio
import datetime
import os
import sys
import uuid

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy.future import select

from app.core.database import async_session_maker
from app.core.security import get_password_hash
from app.models import (
    FinancialPlan,
    InnovationDNA,
    InvestorHub,
    MarketIntelligence,
    ProblemAnalysis,
    Project,
    RiskProfile,
    StartupProfile,
    StartupScore,
    TaskPlanner,
    User,
)


async def seed_data():
    async with async_session_maker() as session:
        # Create Demo User
        result = await session.execute(select(User).filter(User.email == "demo@novax.ai"))
        demo_user = result.scalars().first()
        
        if not demo_user:
            demo_user = User(
                email="demo@novax.ai",
                hashed_password=get_password_hash("Demo@12345"),
                full_name="Demo Judge",
                is_active=True,
                is_superuser=False
            )
            session.add(demo_user)
            await session.commit()
            await session.refresh(demo_user)
            print("Created Demo User: demo@novax.ai / Demo@12345")
        else:
            print("Demo User already exists.")

        # Delete old demo projects if any
        existing_projects_result = await session.execute(select(Project).filter(Project.owner_id == demo_user.id))
        existing_projects = existing_projects_result.scalars().all()
        for ep in existing_projects:
             await session.delete(ep)
        await session.commit()

        # Startup 1: EcoFarm AI
        project1 = Project(
            id=uuid.uuid4(),
            name="EcoFarm AI",
            description="AI-driven precision agriculture for sustainable farming.",
            owner_id=demo_user.id,
            status="Completed",
            completion_percentage=100,
            project_timeline=[{"event": "Created", "date": datetime.datetime.now(datetime.timezone.utc).isoformat()}]
        )

        score1 = StartupScore(
            id=uuid.uuid4(),
            project_id=project1.id,
            innovation_score=92,
            business_score=85,
            market_score=88,
            technology_score=95,
            scalability_score=90,
            execution_score=80,
            financial_score=82,
            investment_readiness=88,
            overall_score=88,
            ai_recommendations={"strengths": ["AI Tech", "Market Timing"], "weaknesses": ["Capital intensive"]}
        )

        prob1 = ProblemAnalysis(
            id=uuid.uuid4(),
            project_id=project1.id,
            core_problem="Farmers lack real-time insights into crop health and soil conditions.",
            problem_summary="Farmers lack real-time insights into crop health and soil conditions, leading to suboptimal yields and excessive water/chemical usage.",
            root_cause_analysis={"causes": ["Manual tracking", "Climate unpredictability"]},
            stakeholders=[{"name": "Commercial Farmers", "type": "Primary"}],
            impact_analysis={"economic": "High", "environmental": "High"},
            existing_alternatives={"list": ["Manual scouting", "Basic weather apps", "Drone imaging (expensive/infrequent)"]},
            opportunity_score=85,
            key_insights=["Focus on water scarcity regions initially"]
        )

        dna1 = InnovationDNA(
            id=uuid.uuid4(),
            project_id=project1.id,
            unique_value_proposition="Increase crop yields by 20% while reducing water usage by 30% through predictive AI.",
            unfair_advantage="Multispectral satellite data combined with ground IoT sensors processed via edge AI.",
            key_innovations=["Edge AI", "Predictive maintenance"],
            technology_stack=["AWS", "IoT Core", "React"],
            innovation_score=90,
            originality_score=85,
            competitor_overview={"competitors": ["CropIn"]},
            market_gap="Lack of real-time insights",
            novelty_analysis="High",
            differentiation={"points": []},
            patent_potential_indicator="High",
            innovation_radar_visualization={}
        )

        profile1 = StartupProfile(
            id=uuid.uuid4(),
            project_id=project1.id,
            name="EcoFarm AI",
            tagline="Intelligence for every acre.",
            mission_statement="To secure global food supply through sustainable, data-driven farming.",
            vision="A world where agriculture operates in perfect harmony with nature.",
            core_values='{"list": ["Sustainability", "Innovation", "Farmer-first", "Data-driven"]}',
            brand_personality='{"voice": "Professional, Innovative, Reliable"}',
            logo_prompt="A leaf with a circuit board.",
            color_palette={"primary": "#4CAF50"},
            value_proposition="Increase yields.",
            unique_selling_proposition="AI driven.",
            elevator_pitch="EcoFarm AI is an intelligent platform that helps commercial farmers increase yields and save water using satellite imagery and IoT sensors powered by edge AI.",
            product_roadmap=[],
            launch_checklist=[]
        )

        market1 = MarketIntelligence(
            id=uuid.uuid4(),
            project_id=project1.id,
            tam_sam_som={"tam": "15B", "sam": "3B", "som": "50M"},
            industry_growth_rate="15",
            cagr="12.5",
            market_maturity="Growing",
            customer_personas=[{"name": "Farmer Joe"}],
            adoption_curve="Early Adopters",
            seasonal_trends='["High in Spring"]',
            market_trends=["Climate change driving water conservation", "Subsidies for smart ag tech"],
            geographic_expansion=["US", "EU"],
            regulatory_risks=["FAA regulations"],
            emerging_technologies=["Edge AI"],
            swot_analysis={"strengths": ["AI models"], "weaknesses": ["Hardware supply chain"], "opportunities": ["Carbon credits"], "threats": ["Regulation"]},
            competitor_matrix={"CropIn": "Established"},
            market_gap_analysis="Real time insight",
            barriers_to_entry=["High hardware cost"],
            market_readiness_score=85,
            ai_metadata={}
        )

        fin1 = FinancialPlan(
            id=uuid.uuid4(),
            project_id=project1.id,
            startup_costs={"r_and_d": "40%", "sales": "40%", "ops": "20%"},
            monthly_operating_costs={"total": 50000},
            hiring_costs={"total": 20000},
            marketing_budget={"total": 10000},
            infrastructure_cost={"total": 5000},
            revenue_forecast={"year1": 500000},
            cash_flow={"year1": 100000},
            burn_rate="20000",
            runway="12",
            break_even_month="18",
            funding_requirement="2000000",
            funding_recommendation="Seed",
            roi_projection="10x",
            ai_metadata={}
        )

        inv1 = InvestorHub(
            id=uuid.uuid4(),
            project_id=project1.id,
            executive_summary="EcoFarm AI is raising $2M seed to scale its smart agriculture platform.",
            investment_memo="Thesis: Agriculture needs AI.",
            funding_strategy="Seed",
            one_page_profile={"summary": "EcoFarm AI is the future."},
            due_diligence_checklist=["Code review", "Patents"],
            milestone_roadmap=["MVP", "First 10 customers"],
            pitch_deck={"slides": [{"title": "Problem", "content": "Farming is inefficient"}, {"title": "Solution", "content": "EcoFarm AI"}]},
            ai_metadata={}
        )

        risk1 = RiskProfile(
            id=uuid.uuid4(),
            project_id=project1.id,
            technical_risks={"level": "Medium", "mitigation": "Redundant sensors"},
            market_risks={"level": "Low", "mitigation": "Target large farms"},
            financial_risks={"level": "High", "mitigation": "Raise $2M"},
            legal_risks={"level": "Low", "mitigation": "Compliance"},
            execution_risks={"level": "High", "mitigation": "Hire COO"},
            hiring_risks={"level": "Medium", "mitigation": "Use recruiters"},
            ai_metadata={}
        )

        task1 = TaskPlanner(
            id=uuid.uuid4(),
            project_id=project1.id,
            immediate_tasks=[{"task": "Incorporate C-Corp"}],
            day_30_plan=[{"task": "MVP release"}],
            day_90_plan=[{"task": "First 10 pilot farms"}],
            month_6_plan=[{"task": "Seed round"}],
            fundraising_timeline={"q3": "Seed round"},
            product_timeline={"q1": "MVP release"},
            ai_metadata={}
        )

        # Append to session
        session.add_all([project1, score1, prob1, dna1, profile1, market1, fin1, inv1, risk1, task1])

        # Startup 2: MedVision
        project2 = Project(id=uuid.uuid4(), name="MedVision", description="AI assistant for radiologists to detect early-stage anomalies.", owner_id=demo_user.id, status="Completed", completion_percentage=100)
        score2 = StartupScore(id=uuid.uuid4(), project_id=project2.id, overall_score=94, innovation_score=98, business_score=90)
        prob2 = ProblemAnalysis(id=uuid.uuid4(), project_id=project2.id, core_problem="Radiologist burnout and missed early-stage cancers.", problem_summary="Burnout")
        dna2 = InnovationDNA(id=uuid.uuid4(), project_id=project2.id, unique_value_proposition="Detect cancer earlier", unfair_advantage="Proprietary dataset", key_innovations=["Deep Learning"], technology_stack=["PyTorch"])
        profile2 = StartupProfile(id=uuid.uuid4(), project_id=project2.id, name="MedVision", tagline="Seeing the unseen in healthcare.", mission_statement="To save lives", vision="Zero missed diagnoses")
        market2 = MarketIntelligence(id=uuid.uuid4(), project_id=project2.id, tam_sam_som={"tam":"20B"}, industry_growth_rate="12", cagr="10", market_maturity="Growing")
        fin2 = FinancialPlan(id=uuid.uuid4(), project_id=project2.id, startup_costs={"x": "y"}, monthly_operating_costs={"x": "y"}, hiring_costs={"x": "y"}, marketing_budget={"x": "y"}, infrastructure_cost={"x": "y"}, revenue_forecast={"year1": 1000}, cash_flow={"year1": 1000}, burn_rate="1000", runway="24", break_even_month="12", funding_requirement="1000000", funding_recommendation="Series A", roi_projection="5x")
        inv2 = InvestorHub(id=uuid.uuid4(), project_id=project2.id, executive_summary="MedVision Exec Summary")
        risk2 = RiskProfile(id=uuid.uuid4(), project_id=project2.id, technical_risks={"level": "Low"}, market_risks={"level": "Low"}, financial_risks={"level": "Low"}, legal_risks={"level": "Low"}, execution_risks={"level": "Low"}, hiring_risks={"level": "Low"})
        task2 = TaskPlanner(id=uuid.uuid4(), project_id=project2.id, immediate_tasks=[{"task": "Hire CTO"}])

        session.add_all([project2, score2, prob2, dna2, profile2, market2, fin2, inv2, risk2, task2])
        
        # Startup 3: EduNova
        project3 = Project(id=uuid.uuid4(), name="EduNova", description="Hyper-personalized AI tutor for K-12 students.", owner_id=demo_user.id, status="Completed", completion_percentage=100)
        score3 = StartupScore(id=uuid.uuid4(), project_id=project3.id, overall_score=85, innovation_score=82, business_score=88)
        prob3 = ProblemAnalysis(id=uuid.uuid4(), project_id=project3.id, core_problem="One-size-fits-all education leaves behind students who learn differently.", problem_summary="One-size-fits-all education")
        dna3 = InnovationDNA(id=uuid.uuid4(), project_id=project3.id, unique_value_proposition="Personalized tutor", unfair_advantage="Adaptive algorithm", key_innovations=["Generative AI"], technology_stack=["OpenAI API"])
        profile3 = StartupProfile(id=uuid.uuid4(), project_id=project3.id, name="EduNova", tagline="Education that adapts to you.", mission_statement="To democratize education", vision="A world where every student thrives")
        market3 = MarketIntelligence(id=uuid.uuid4(), project_id=project3.id, tam_sam_som={"tam":"80B"}, industry_growth_rate="8", cagr="7", market_maturity="Mature")
        fin3 = FinancialPlan(id=uuid.uuid4(), project_id=project3.id, startup_costs={"x": "y"}, monthly_operating_costs={"x": "y"}, hiring_costs={"x": "y"}, marketing_budget={"x": "y"}, infrastructure_cost={"x": "y"}, revenue_forecast={"year1": 500}, cash_flow={"year1": 500}, burn_rate="500", runway="18", break_even_month="14", funding_requirement="500000", funding_recommendation="Seed", roi_projection="3x")
        inv3 = InvestorHub(id=uuid.uuid4(), project_id=project3.id, executive_summary="EduNova Exec Summary")
        risk3 = RiskProfile(id=uuid.uuid4(), project_id=project3.id, technical_risks={"level": "Low"}, market_risks={"level": "Low"}, financial_risks={"level": "Low"}, legal_risks={"level": "Low"}, execution_risks={"level": "Low"}, hiring_risks={"level": "Low"})
        task3 = TaskPlanner(id=uuid.uuid4(), project_id=project3.id, immediate_tasks=[{"task": "Launch MVP"}])

        session.add_all([project3, score3, prob3, dna3, profile3, market3, fin3, inv3, risk3, task3])

        await session.commit()
        print("Demo data seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_data())
