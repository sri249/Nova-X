import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models import (
    FinancialPlan,
    InnovationDNA,
    InvestorHub,
    MarketIntelligence,
    ProblemAnalysis,
    RiskProfile,
    StartupProfile,
    TaskPlanner,
)

for model in [ProblemAnalysis, InnovationDNA, StartupProfile, MarketIntelligence, FinancialPlan, InvestorHub, RiskProfile, TaskPlanner]:
    print(model.__name__)
    print(model.__table__.columns.keys())
    print("-" * 20)
