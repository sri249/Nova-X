# NOVA X - Architecture Documentation

## Overview
NOVA X is structured as a decoupled microservices-lite architecture relying on a centralized async PostgreSQL store and an isolated AI integration layer.

## 1. Frontend (Next.js)
- **App Router paradigm**: Pages are grouped securely under `(auth)` and `(dashboard)` routing groups.
- **State Management**: React Context (`AuthContext`) manages JWT lifecycles. Server-side rendering (SSR) is utilized where SEO or initial-load speed is critical, while Client Components are used heavily for interactive modules (e.g. Charts, Chat).
- **Styling**: Tailwind CSS v4 provides atomic utility classes. The design system is highly responsive, featuring dynamic dark mode and complex micro-animations for a premium user experience.

## 2. Backend (FastAPI)
- **Modular Monolith**: The application resides in `backend/app/features/`, isolating domain logic (e.g., `projects`, `financial_planner`, `market_intelligence`).
- **Dependency Injection**: Heavy reliance on FastAPI's `Depends()` for DB session provisioning (`get_db_session`) and Auth (`get_current_user`).
- **Asynchronous IO**: Entirely built on `asyncio`. `asyncpg` powers the SQLAlchemy ORM for unblocked, high-concurrency database queries.

## 3. Database (PostgreSQL via Neon)
- **Data Integrity**: Enforced through SQLAlchemy 2.0 mapped models. Core relationship revolves around the `Project` model, utilizing `One-to-One` relationships with all analytical outputs (`FinancialPlan`, `RiskProfile`, etc.).
- **Migrations**: Alembic manages schema versions.

## 4. AI Layer (OpenAI + LangChain)
- **Structured Outputs**: FastAPI leverages OpenAI's structured JSON response capabilities via Pydantic schemas. 
- **Agentic Workflow**: Features like `Startup Formation` use context chains where the output of the `Problem Discovery` API informs the prompt for the `Innovation DNA` API.
- **Persistent Memory**: Chat endpoints utilize LangGraph checkpoints to maintain conversation state, enabling a true "Co-Founder" experience that remembers earlier interactions.

## 5. Authentication
- **JWT Bearer**: OAuth2 standard implementation. Passwords hashed using `passlib(bcrypt)`.
- **Demo Mode**: Bypass logic that issues short-lived mock tokens mapped to a persistent `demo@novax.ai` account for hackathon judges.

## 6. Export System
- **PDF Generation**: HTML template rendered server-side containing full analytical breakdowns, utilizing frontend `window.print()` interception for high-fidelity PDF saves.
- **Pitch Deck JSON**: Programmatic structuring of DB state into a standardized JSON format meant for consumption by presentation-generation libraries.
