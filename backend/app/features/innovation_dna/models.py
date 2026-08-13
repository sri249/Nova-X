import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class InnovationDNA(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "innovation_dna"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    unique_value_proposition: Mapped[str] = mapped_column(String)
    unfair_advantage: Mapped[str] = mapped_column(String)
    key_innovations: Mapped[dict] = mapped_column(JSONB, default=list)
    technology_stack: Mapped[dict] = mapped_column(JSONB, default=list)
    innovation_score: Mapped[int] = mapped_column(Integer, nullable=True)
    originality_score: Mapped[int] = mapped_column(Integer, nullable=True)
    competitor_overview: Mapped[list] = mapped_column(JSONB, default=list)
    market_gap: Mapped[str] = mapped_column(Text, nullable=True)
    novelty_analysis: Mapped[str] = mapped_column(Text, nullable=True)
    differentiation: Mapped[list] = mapped_column(JSONB, default=list)
    patent_potential_indicator: Mapped[str] = mapped_column(String, nullable=True)
    innovation_radar_visualization: Mapped[dict] = mapped_column(JSONB, default=dict)

    project = relationship("Project", back_populates="innovation_dna")
