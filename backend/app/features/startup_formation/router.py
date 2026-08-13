import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.dependencies import get_current_user
from app.core.database import get_db_session
from app.features.innovation_dna.models import InnovationDNA
from app.features.problem_discovery.models import ProblemAnalysis
from app.features.projects.models import AIVersionHistory, Project
from app.features.projects.utils import recalculate_project_completion
from app.features.startup_formation.models import (
    BusinessModel,
    CustomerPersona,
    StartupProfile,
)
from app.features.startup_formation.schemas import (
    SingleFieldRegenerateResponse,
    SingleFieldUpdate,
    StartupFormationResponse,
)
from app.features.users.models import User
from app.services.ai import ContextManager, ai_service

router = APIRouter(prefix="/projects/{project_id}/startup-formation", tags=["startup_formation"])

@router.post("", response_model=StartupFormationResponse)
async def generate_startup_formation(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    problem_result = await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))
    problem = problem_result.scalars().first()
    dna_result = await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))
    dna = dna_result.scalars().first()

    if not problem or not dna:
        raise HTTPException(status_code=400, detail="Problem Discovery and Innovation DNA must be completed first")

    # Generate via AI
    ai_output = await ai_service.generate_startup_formation(
        problem_data=problem.core_problem,
        innovation_data=dna.unique_value_proposition
    )

    # Save to database
    existing_profile = (await db.execute(select(StartupProfile).where(StartupProfile.project_id == project_id))).scalars().first()
    
    if existing_profile:
        existing_profile.name = ai_output.startup_name
        existing_profile.tagline = ai_output.tagline
        existing_profile.mission_statement = ai_output.mission
        existing_profile.vision = ai_output.vision
        existing_profile.core_values = ai_output.core_values
        existing_profile.brand_personality = ai_output.brand_personality
        existing_profile.logo_prompt = ai_output.logo_prompt
        existing_profile.color_palette = ai_output.color_palette
        existing_profile.value_proposition = ai_output.value_proposition
        existing_profile.unique_selling_proposition = ai_output.unique_selling_proposition
        existing_profile.elevator_pitch = ai_output.elevator_pitch
        existing_profile.product_roadmap = ai_output.product_roadmap
        existing_profile.launch_checklist = ai_output.launch_checklist
        profile = existing_profile
    else:
        profile = StartupProfile(
            project_id=project_id,
            name=ai_output.startup_name,
            tagline=ai_output.tagline,
            mission_statement=ai_output.mission,
            vision=ai_output.vision,
            core_values=ai_output.core_values,
            brand_personality=ai_output.brand_personality,
            logo_prompt=ai_output.logo_prompt,
            color_palette=ai_output.color_palette,
            value_proposition=ai_output.value_proposition,
            unique_selling_proposition=ai_output.unique_selling_proposition,
            elevator_pitch=ai_output.elevator_pitch,
            product_roadmap=ai_output.product_roadmap,
            launch_checklist=ai_output.launch_checklist
        )
        db.add(profile)

    existing_bm = (await db.execute(select(BusinessModel).where(BusinessModel.project_id == project_id))).scalars().first()
    if existing_bm:
        existing_bm.revenue_streams = [ai_output.revenue_model]
        existing_bm.cost_structure = [ai_output.business_model_canvas]
        existing_bm.pricing_strategy = ai_output.pricing_strategy
        existing_bm.go_to_market = ai_output.launch_checklist[0] if ai_output.launch_checklist else None
        existing_bm.business_model_canvas = ai_output.business_model_canvas
        existing_bm.revenue_model = ai_output.revenue_model
        bm = existing_bm
    else:
        bm = BusinessModel(
            project_id=project_id,
            revenue_streams=[ai_output.revenue_model],
            cost_structure=[ai_output.business_model_canvas],
            pricing_strategy=ai_output.pricing_strategy,
            go_to_market=ai_output.launch_checklist[0] if ai_output.launch_checklist else None,
            business_model_canvas=ai_output.business_model_canvas,
            revenue_model=ai_output.revenue_model
        )
        db.add(bm)

    # Simplified Customer Persona (Just creating one for the output)
    persona = CustomerPersona(
        project_id=project_id,
        name="Target User",
        demographics=ai_output.customer_persona,
        pain_points=[],
        goals=[]
    )
    db.add(persona)

    await db.commit()
    await db.refresh(profile)
    await db.refresh(bm)
    await db.refresh(persona)

    await recalculate_project_completion(project_id, db)
    return {
        "profile": profile,
        "business_model": bm,
        "personas": [persona]
    }

@router.get("")
async def get_startup_formation(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    profile = (await db.execute(select(StartupProfile).where(StartupProfile.project_id == project_id))).scalars().first()
    bm = (await db.execute(select(BusinessModel).where(BusinessModel.project_id == project_id))).scalars().first()
    persona = (await db.execute(select(CustomerPersona).where(CustomerPersona.project_id == project_id))).scalars().first()

    if not profile or not bm:
        raise HTTPException(status_code=404, detail="Startup Formation not found")

    return {
        "profile": profile,
        "business_model": bm,
        "personas": [persona] if persona else []
    }

@router.put("/{model}/{field_name}")
async def update_single_field(
    project_id: uuid.UUID,
    model: str,
    field_name: str,
    update_data: SingleFieldUpdate,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    model_class = {"profile": StartupProfile, "business_model": BusinessModel, "persona": CustomerPersona}.get(model)
    if not model_class:
        raise HTTPException(status_code=400, detail="Invalid model")

    existing_result = await db.execute(select(model_class).where(model_class.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    if not hasattr(existing, field_name):
        raise HTTPException(status_code=400, detail=f"Field {field_name} does not exist")
        
    setattr(existing, field_name, update_data.content)
    await db.commit()
    await db.refresh(existing)
    return {"status": "updated", "field": field_name, "content": update_data.content}

@router.post("/{model}/{field_name}/regenerate", response_model=SingleFieldRegenerateResponse)
async def regenerate_single_field(
    project_id: uuid.UUID,
    model: str,
    field_name: str,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    model_class = {"profile": StartupProfile, "business_model": BusinessModel, "persona": CustomerPersona}.get(model)
    if not model_class:
        raise HTTPException(status_code=400, detail="Invalid model")

    existing_result = await db.execute(select(model_class).where(model_class.project_id == project_id))
    existing = existing_result.scalars().first()
    if not existing or not hasattr(existing, field_name):
        raise HTTPException(status_code=404, detail="Field or Entity not found")

    current_content = getattr(existing, field_name)
    
    history = AIVersionHistory(
        project_id=project_id,
        module=f"startup_{model}",
        field_name=field_name,
        content={"data": current_content} if not isinstance(current_content, dict) else current_content
    )
    db.add(history)

    problem = (await db.execute(select(ProblemAnalysis).where(ProblemAnalysis.project_id == project_id))).scalars().first()
    dna = (await db.execute(select(InnovationDNA).where(InnovationDNA.project_id == project_id))).scalars().first()
    
    context_str = ContextManager.build_full_context(
        {"core": problem.problem_summary} if problem else {},
        {"dna": dna.unique_value_proposition} if dna else {},
        {field_name: getattr(existing, field_name, None)}
    )
    
    new_content = await ai_service.regenerate_single_field(context_str, field_name, str(current_content))
    
    if isinstance(current_content, (dict, list)):
        try:
            new_content = json.loads(new_content)
        except json.JSONDecodeError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("Failed to decode JSON: %s", e)

    setattr(existing, field_name, new_content)
    await db.commit()
    
    return SingleFieldRegenerateResponse(new_content=new_content)
