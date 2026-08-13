import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Project(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String, default="Draft") # Draft, Generating, Completed, Archived
    completion_percentage: Mapped[int] = mapped_column(Integer, default=0)
    project_timeline: Mapped[list] = mapped_column(JSONB, default=list)

    # Relationships
    owner = relationship("User", back_populates="projects")
    problem_analysis = relationship("ProblemAnalysis", back_populates="project", uselist=False, cascade="all, delete-orphan")
    innovation_dna = relationship("InnovationDNA", back_populates="project", uselist=False, cascade="all, delete-orphan")
    startup_profile = relationship("StartupProfile", back_populates="project", uselist=False, cascade="all, delete-orphan")
    business_model = relationship("BusinessModel", back_populates="project", uselist=False, cascade="all, delete-orphan")
    customer_personas = relationship("CustomerPersona", back_populates="project", cascade="all, delete-orphan")
    market_intelligence = relationship("MarketIntelligence", back_populates="project", uselist=False, cascade="all, delete-orphan")
    financial_plan = relationship("FinancialPlan", back_populates="project", uselist=False, cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="project", cascade="all, delete-orphan")
    startup_score = relationship("StartupScore", back_populates="project", uselist=False, cascade="all, delete-orphan")
    version_histories = relationship("AIVersionHistory", back_populates="project", cascade="all, delete-orphan")
    
    # Phase 5
    investor_hub = relationship("InvestorHub", back_populates="project", uselist=False, cascade="all, delete-orphan")
    risk_profile = relationship("RiskProfile", back_populates="project", uselist=False, cascade="all, delete-orphan")
    task_planner = relationship("TaskPlanner", back_populates="project", uselist=False, cascade="all, delete-orphan")
    ai_mentor_analysis = relationship("AIMentorAnalysis", back_populates="project", uselist=False, cascade="all, delete-orphan")

class StartupScore(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "startup_scores"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), unique=True)
    innovation_score: Mapped[int] = mapped_column(Integer, default=0)
    business_score: Mapped[int] = mapped_column(Integer, default=0)
    market_score: Mapped[int] = mapped_column(Integer, default=0)
    technology_score: Mapped[int] = mapped_column(Integer, default=0)
    scalability_score: Mapped[int] = mapped_column(Integer, default=0)
    execution_score: Mapped[int] = mapped_column(Integer, default=0)
    financial_score: Mapped[int] = mapped_column(Integer, default=0)
    investment_readiness: Mapped[int] = mapped_column(Integer, default=0)
    overall_score: Mapped[int] = mapped_column(Integer, default=0)
    ai_recommendations: Mapped[dict] = mapped_column(JSONB, default=dict)

    project = relationship("Project", back_populates="startup_score")

class AIVersionHistory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "ai_version_history"

    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    module: Mapped[str] = mapped_column(String) # e.g., 'problem_discovery'
    field_name: Mapped[str] = mapped_column(String) # e.g., 'problem_summary'
    content: Mapped[dict] = mapped_column(JSONB) # The previous content (can be string or dict)

    project = relationship("Project", back_populates="version_histories")
