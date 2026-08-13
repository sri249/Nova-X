import uuid
from datetime import datetime

from pydantic import BaseModel


class StartupProfileResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    tagline: str | None
    mission_statement: str | None
    vision: str | None
    core_values: list
    brand_personality: str | None
    logo_prompt: str | None
    color_palette: list
    value_proposition: str | None
    unique_selling_proposition: str | None
    elevator_pitch: str | None
    product_roadmap: list
    launch_checklist: list
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BusinessModelResponse(BaseModel):
    id: uuid.UUID
    revenue_streams: list
    cost_structure: list
    pricing_strategy: str | None
    go_to_market: str | None
    business_model_canvas: dict
    revenue_model: dict

    class Config:
        from_attributes = True

class CustomerPersonaResponse(BaseModel):
    id: uuid.UUID
    name: str
    demographics: dict
    pain_points: list
    goals: list

    class Config:
        from_attributes = True

class StartupFormationResponse(BaseModel):
    profile: StartupProfileResponse
    business_model: BusinessModelResponse
    personas: list[CustomerPersonaResponse]

class SingleFieldUpdate(BaseModel):
    content: str | dict | list

class SingleFieldRegenerateResponse(BaseModel):
    new_content: str | dict | list
