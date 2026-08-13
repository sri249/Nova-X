import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, TimestampMixin, UUIDMixin


class StartupProfile(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "startup_profiles"
    
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    name: Mapped[str] = mapped_column(String)
    tagline: Mapped[str] = mapped_column(String, nullable=True)
    mission_statement: Mapped[str] = mapped_column(String, nullable=True)
    vision: Mapped[str] = mapped_column(String, nullable=True)
    core_values: Mapped[list] = mapped_column(JSONB, default=list)
    brand_personality: Mapped[str] = mapped_column(String, nullable=True)
    logo_prompt: Mapped[str] = mapped_column(Text, nullable=True)
    color_palette: Mapped[list] = mapped_column(JSONB, default=list)
    value_proposition: Mapped[str] = mapped_column(Text, nullable=True)
    unique_selling_proposition: Mapped[str] = mapped_column(Text, nullable=True)
    elevator_pitch: Mapped[str] = mapped_column(Text, nullable=True)
    product_roadmap: Mapped[list] = mapped_column(JSONB, default=list)
    launch_checklist: Mapped[list] = mapped_column(JSONB, default=list)
    
    project = relationship("Project", back_populates="startup_profile")

class BusinessModel(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "business_models"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    revenue_streams: Mapped[list] = mapped_column(JSONB, default=list)
    cost_structure: Mapped[list] = mapped_column(JSONB, default=list)
    pricing_strategy: Mapped[str] = mapped_column(String, nullable=True)
    go_to_market: Mapped[str] = mapped_column(String, nullable=True)
    business_model_canvas: Mapped[dict] = mapped_column(JSONB, default=dict)
    revenue_model: Mapped[dict] = mapped_column(JSONB, default=dict)

    project = relationship("Project", back_populates="business_model")

class CustomerPersona(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "customer_personas"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    name: Mapped[str] = mapped_column(String)
    demographics: Mapped[dict] = mapped_column(JSONB, default=dict)
    pain_points: Mapped[list] = mapped_column(JSONB, default=list)
    goals: Mapped[list] = mapped_column(JSONB, default=list)

    project = relationship("Project", back_populates="customer_personas")
