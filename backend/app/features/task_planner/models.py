import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class TaskPlanner(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "task_planner"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    
    # Arrays of tasks
    immediate_tasks: Mapped[list | None] = mapped_column(JSON, default=None)
    day_30_plan: Mapped[list | None] = mapped_column(JSON, default=None)
    day_90_plan: Mapped[list | None] = mapped_column(JSON, default=None)
    month_6_plan: Mapped[list | None] = mapped_column(JSON, default=None)
    fundraising_timeline: Mapped[list | None] = mapped_column(JSON, default=None)
    product_timeline: Mapped[list | None] = mapped_column(JSON, default=None)
    
    ai_metadata: Mapped[dict | None] = mapped_column(JSON, default=None)

    project = relationship("Project", back_populates="task_planner")
