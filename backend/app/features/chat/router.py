import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.chat.models import ChatHistory
from app.features.projects.models import Project
from app.features.users.models import User
from app.features.users.router import get_current_user
from app.services.ai.context_manager import ContextManager
from app.services.ai.service import ai_service

router = APIRouter(prefix="/projects/{project_id}/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    message: str
    session_id: str

@router.post("")
async def send_chat_message(
    project_id: uuid.UUID,
    payload: ChatMessage,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = project_result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Save user message
    user_msg = ChatHistory(
        project_id=project_id,
        session_id=payload.session_id,
        role="user",
        content=payload.message
    )
    db.add(user_msg)
    await db.commit()

    # Get history for this session
    history_result = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.project_id == project_id, ChatHistory.session_id == payload.session_id)
        .order_by(ChatHistory.created_at)
    )
    history = history_result.scalars().all()
    messages_payload = [{"role": h.role, "content": h.content} for h in history]

    context = await ContextManager.build_full_project_context(project_id, db)
    
    # In a real app we'd stream this, but for now we'll wait for the full response
    response_content = await ai_service.generate_co_founder_chat(context=context, messages=messages_payload)

    # Save assistant message
    assistant_msg = ChatHistory(
        project_id=project_id,
        session_id=payload.session_id,
        role="assistant",
        content=response_content
    )
    db.add(assistant_msg)
    await db.commit()

    return {"status": "success", "response": response_content}

@router.get("/{session_id}")
async def get_chat_history(
    project_id: uuid.UUID,
    session_id: str,
    current_user: User = Depends(get_current_user), 
    db: AsyncSession = Depends(get_db_session)
):
    project_result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    if not project_result.scalars().first():
        raise HTTPException(status_code=404, detail="Project not found")

    result = await db.execute(
        select(ChatHistory)
        .where(ChatHistory.project_id == project_id, ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at)
    )
    return result.scalars().all()
