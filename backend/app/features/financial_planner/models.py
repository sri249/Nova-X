import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class FinancialPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "financial_plans"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    
    startup_costs: Mapped[dict] = mapped_column(JSONB, default=dict)
    monthly_operating_costs: Mapped[dict] = mapped_column(JSONB, default=dict)
    hiring_costs: Mapped[dict] = mapped_column(JSONB, default=dict)
    marketing_budget: Mapped[dict] = mapped_column(JSONB, default=dict)
    infrastructure_cost: Mapped[dict] = mapped_column(JSONB, default=dict)
    revenue_forecast: Mapped[list] = mapped_column(JSONB, default=list)
    cash_flow: Mapped[list] = mapped_column(JSONB, default=list)
    
    burn_rate: Mapped[str] = mapped_column(String, nullable=True)
    runway: Mapped[str] = mapped_column(String, nullable=True)
    break_even_month: Mapped[str] = mapped_column(String, nullable=True)
    funding_requirement: Mapped[str] = mapped_column(String, nullable=True)
    funding_recommendation: Mapped[Text] = mapped_column(Text, nullable=True)
    roi_projection: Mapped[str] = mapped_column(String, nullable=True)

    ai_metadata: Mapped[dict] = mapped_column(JSONB, default=dict) # Confidence Score, Sources, etc.

    project = relationship("Project", back_populates="financial_plan")
