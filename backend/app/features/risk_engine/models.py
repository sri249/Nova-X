import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class RiskProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "risk_profile"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    
    # Arrays of dictionaries detailing Level, Impact, Probability, Mitigation Plan
    technical_risks: Mapped[list | None] = mapped_column(JSON, default=None)
    market_risks: Mapped[list | None] = mapped_column(JSON, default=None)
    financial_risks: Mapped[list | None] = mapped_column(JSON, default=None)
    legal_risks: Mapped[list | None] = mapped_column(JSON, default=None)
    execution_risks: Mapped[list | None] = mapped_column(JSON, default=None)
    hiring_risks: Mapped[list | None] = mapped_column(JSON, default=None)
    
    ai_metadata: Mapped[dict | None] = mapped_column(JSON, default=None)

    project = relationship("Project", back_populates="risk_profile")
