import uuid
from datetime import datetime

from pydantic import BaseModel


class InnovationDNAResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    unique_value_proposition: str
    unfair_advantage: str
    key_innovations: list | None = None
    technology_stack: list | None = None
    innovation_score: int | None
    originality_score: int | None
    competitor_overview: list
    market_gap: str | None
    novelty_analysis: str | None
    differentiation: list
    patent_potential_indicator: str | None
    innovation_radar_visualization: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SingleFieldUpdate(BaseModel):
    content: str | dict | list

class SingleFieldRegenerateResponse(BaseModel):
    new_content: str | dict | list
