import uuid

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class ProblemAnalysis(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "problem_analysis"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    core_problem: Mapped[str] = mapped_column(Text)
    problem_summary: Mapped[str] = mapped_column(Text, nullable=True)
    root_cause_analysis: Mapped[dict] = mapped_column(JSONB, default=dict)
    stakeholders: Mapped[list] = mapped_column(JSONB, default=list)
    impact_analysis: Mapped[dict] = mapped_column(JSONB, default=dict)
    existing_alternatives: Mapped[dict] = mapped_column(JSONB, default=dict)
    impact_metrics: Mapped[dict] = mapped_column(JSONB, default=dict) # Legacy? keeping it
    opportunity_score: Mapped[int] = mapped_column(Integer, nullable=True)
    sdg_alignment: Mapped[list] = mapped_column(JSONB, default=list)
    key_insights: Mapped[list] = mapped_column(JSONB, default=list)

    project = relationship("Project", back_populates="problem_analysis")
