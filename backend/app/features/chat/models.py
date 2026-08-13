import uuid

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class ChatHistory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "chat_history"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    session_id: Mapped[str] = mapped_column(String, index=True)
    role: Mapped[str] = mapped_column(String) # user, assistant, system
    content: Mapped[str] = mapped_column(String)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict, nullable=True)

    project = relationship("Project", back_populates="chat_histories")
