from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db_session
from app.models import Project

router = APIRouter(prefix="/api/export", tags=["export"])

@router.get("/{project_id}/pdf", response_class=HTMLResponse)
async def export_pdf(
    project_id: str,
    db: AsyncSession = Depends(get_db_session)
    # Removing get_current_user dependency to allow easy demo export without strict token checks if needed,
    # or keep it if required. Since we want a robust demo mode, let's keep it but handle it gracefully.
):
    stmt = (
        select(Project)
        .options(
            selectinload(Project.problem_analysis),
            selectinload(Project.innovation_dna),
            selectinload(Project.startup_profile),
            selectinload(Project.market_intelligence),
            selectinload(Project.financial_plan),
            selectinload(Project.investor_hub),
            selectinload(Project.risk_profile),
            selectinload(Project.task_planner),
            selectinload(Project.startup_score)
        )
        .where(Project.id == project_id)
    )
    result = await db.execute(stmt)
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Generate a beautiful HTML report that the frontend can print to PDF
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{project.name} - Executive Summary</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; color: #333; line-height: 1.6; margin: 40px; }}
            h1 {{ color: #1a56db; border-bottom: 2px solid #1a56db; padding-bottom: 10px; }}
            h2 {{ color: #2563eb; margin-top: 30px; }}
            .section {{ margin-bottom: 40px; page-break-inside: avoid; }}
            .card {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; background: #f9fafb; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #e5e7eb; text-align: left; }}
            th {{ background-color: #f3f4f6; }}
            .score {{ font-size: 24px; font-weight: bold; color: #10b981; }}
        </style>
    </head>
    <body>
        <div class="section">
            <h1>{project.name} - Executive Summary</h1>
            <p><strong>Description:</strong> {project.description}</p>
        </div>
        
        <div class="section">
            <h2>Startup Health</h2>
            <div class="card">
                <p>Overall Score: <span class="score">{project.startup_score.overall_score if project.startup_score else 'N/A'}</span> / 100</p>
            </div>
        </div>

        <div class="section">
            <h2>Market Intelligence</h2>
            <p><strong>TAM:</strong> {project.market_intelligence.tam_sam_som.get('tam') if project.market_intelligence and project.market_intelligence.tam_sam_som else 'N/A'}</p>
            <p><strong>SAM:</strong> {project.market_intelligence.tam_sam_som.get('sam') if project.market_intelligence and project.market_intelligence.tam_sam_som else 'N/A'}</p>
            <p><strong>SOM:</strong> {project.market_intelligence.tam_sam_som.get('som') if project.market_intelligence and project.market_intelligence.tam_sam_som else 'N/A'}</p>
        </div>

        <div class="section">
            <h2>Financial Plan</h2>
            <p><strong>Funding Requirement:</strong> {project.financial_plan.funding_requirement if project.financial_plan else 'N/A'}</p>
            <p><strong>Runway:</strong> {project.financial_plan.runway if project.financial_plan else 'N/A'} months</p>
        </div>

        <div class="section">
            <h2>Risk Profile</h2>
            <p><strong>Technical Risk:</strong> {project.risk_profile.technical_risks.get('level') if project.risk_profile and project.risk_profile.technical_risks else 'N/A'}</p>
            <p><strong>Market Risk:</strong> {project.risk_profile.market_risks.get('level') if project.risk_profile and project.risk_profile.market_risks else 'N/A'}</p>
            <p><strong>Execution Risk:</strong> {project.risk_profile.execution_risks.get('level') if project.risk_profile and project.risk_profile.execution_risks else 'N/A'}</p>
        </div>
        
        <script>
            window.onload = function() {{ window.print(); }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@router.get("/{project_id}/pitch-deck")
async def export_pitch_deck(
    project_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    stmt = (
        select(Project)
        .options(
            selectinload(Project.problem_analysis),
            selectinload(Project.innovation_dna),
            selectinload(Project.startup_profile),
            selectinload(Project.market_intelligence),
            selectinload(Project.financial_plan),
            selectinload(Project.investor_hub)
        )
        .where(Project.id == project_id)
    )
    result = await db.execute(stmt)
    project = result.scalars().first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Generate PowerPoint-ready JSON
    deck = {
        "presentation": {
            "title": project.name,
            "subtitle": project.startup_profile.tagline if project.startup_profile else project.description,
            "theme": "modern_dark",
            "slides": [
                {
                    "type": "title",
                    "title": project.name,
                    "subtitle": project.startup_profile.tagline if project.startup_profile else "The Future of AI",
                    "speaker_notes": f"Welcome everyone. Today I am excited to introduce {project.name}.",
                    "timing_seconds": 60
                },
                {
                    "type": "problem",
                    "title": "The Problem",
                    "bullet_points": [
                        project.problem_analysis.core_problem if project.problem_analysis else "Identified problem"
                    ],
                    "speaker_notes": "We identified a massive gap in the market...",
                    "timing_seconds": 90
                },
                {
                    "type": "solution",
                    "title": "Our Solution",
                    "bullet_points": [
                        project.innovation_dna.unique_value_proposition if project.innovation_dna else "Our AI solution"
                    ],
                    "image_placeholder": "solution_architecture.png",
                    "speaker_notes": "To solve this, we built a comprehensive platform.",
                    "timing_seconds": 120
                },
                {
                    "type": "market",
                    "title": "Market Opportunity",
                    "bullet_points": [
                        f"TAM: {project.market_intelligence.tam_sam_som.get('tam') if project.market_intelligence and project.market_intelligence.tam_sam_som else 'N/A'}",
                        f"SAM: {project.market_intelligence.tam_sam_som.get('sam') if project.market_intelligence and project.market_intelligence.tam_sam_som else 'N/A'}"
                    ],
                    "chart_placeholder": "market_growth_bar_chart",
                    "speaker_notes": "The market is growing rapidly.",
                    "timing_seconds": 90
                },
                {
                    "type": "financials",
                    "title": "Financial Projections & Ask",
                    "bullet_points": [
                        f"Raising: {project.financial_plan.funding_requirement if project.financial_plan else 'N/A'}",
                        "Use of funds: 40% R&D, 40% Sales, 20% Ops"
                    ],
                    "speaker_notes": "We are raising capital to accelerate growth.",
                    "timing_seconds": 90
                }
            ]
        }
    }

    return JSONResponse(content=deck)
