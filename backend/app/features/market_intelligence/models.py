import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class MarketIntelligence(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "market_intelligence"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    
    tam_sam_som: Mapped[dict] = mapped_column(JSONB, default=dict)
    industry_growth_rate: Mapped[str] = mapped_column(String, nullable=True)
    cagr: Mapped[str] = mapped_column(String, nullable=True)
    market_maturity: Mapped[str] = mapped_column(String, nullable=True)
    customer_personas: Mapped[list] = mapped_column(JSONB, default=list)
    adoption_curve: Mapped[str] = mapped_column(String, nullable=True)
    seasonal_trends: Mapped[str] = mapped_column(String, nullable=True)
    market_trends: Mapped[list] = mapped_column(JSONB, default=list)
    geographic_expansion: Mapped[list] = mapped_column(JSONB, default=list)
    regulatory_risks: Mapped[list] = mapped_column(JSONB, default=list)
    emerging_technologies: Mapped[list] = mapped_column(JSONB, default=list)
    swot_analysis: Mapped[dict] = mapped_column(JSONB, default=dict)
    competitor_matrix: Mapped[list] = mapped_column(JSONB, default=list)
    market_gap_analysis: Mapped[str] = mapped_column(Text, nullable=True)
    barriers_to_entry: Mapped[list] = mapped_column(JSONB, default=list)
    market_readiness_score: Mapped[int] = mapped_column(Integer, nullable=True)
    
    ai_metadata: Mapped[dict] = mapped_column(JSONB, default=dict) # Confidence Score, Sources, etc.

    project = relationship("Project", back_populates="market_intelligence")
