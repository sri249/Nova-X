import uuid
from datetime import datetime

from pydantic import BaseModel


class ProblemDiscoveryInput(BaseModel):
    title: str
    description: str
    industry: str
    country: str
    target_users: str
    existing_solutions: str
    pain_points: str

class ProblemDiscoveryResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    core_problem: str
    problem_summary: str | None
    root_cause_analysis: dict
    stakeholders: list
    impact_analysis: dict
    existing_alternatives: dict
    impact_metrics: dict
    opportunity_score: int | None
    sdg_alignment: list
    key_insights: list
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SingleFieldUpdate(BaseModel):
    content: str | dict | list

class SingleFieldRegenerateResponse(BaseModel):
    new_content: str | dict | list
