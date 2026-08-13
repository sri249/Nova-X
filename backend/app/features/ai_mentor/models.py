import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class AIMentorAnalysis(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_mentor_analysis"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    
    strengths: Mapped[list | None] = mapped_column(JSON, default=None)
    weaknesses: Mapped[list | None] = mapped_column(JSON, default=None)
    missing_information: Mapped[list | None] = mapped_column(JSON, default=None)
    risk_alerts: Mapped[list | None] = mapped_column(JSON, default=None) # [{ level: high/medium/low, alert: string }]
    recommended_next_actions: Mapped[list | None] = mapped_column(JSON, default=None)
    weekly_priorities: Mapped[list | None] = mapped_column(JSON, default=None)
    
    ai_metadata: Mapped[dict | None] = mapped_column(JSON, default=None)

    project = relationship("Project", back_populates="ai_mentor_analysis")
