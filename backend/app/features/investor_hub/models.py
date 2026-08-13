import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class InvestorHub(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "investor_hub"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    
    # Generated sections
    executive_summary: Mapped[str | None] = mapped_column(default=None)
    investment_memo: Mapped[str | None] = mapped_column(default=None)
    funding_strategy: Mapped[str | None] = mapped_column(default=None)
    
    # JSON arrays/objects
    one_page_profile: Mapped[dict | None] = mapped_column(JSON, default=None)
    due_diligence_checklist: Mapped[list | None] = mapped_column(JSON, default=None)
    milestone_roadmap: Mapped[list | None] = mapped_column(JSON, default=None)
    pitch_deck: Mapped[dict | None] = mapped_column(JSON, default=None) # The structured JSON for slides
    
    ai_metadata: Mapped[dict | None] = mapped_column(JSON, default=None)

    project = relationship("Project", back_populates="investor_hub")
