# NOVA X - Administrator Guide

## 1. Environment Variables
To securely run NOVA X, the following environment variables must be injected into the respective environments.

### Backend (`backend/.env`)
*   `DATABASE_URL`: Must be an `asyncpg` compatible connection string (e.g., `postgresql+asyncpg://user:pass@host/db`).
*   `SECRET_KEY`: A high-entropy string for signing JWT tokens.
*   `ALGORITHM`: JWT Algorithm (Default: `HS256`).
*   `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT Lifespan (Default: `30`).
*   `OPENAI_API_KEY`: A valid OpenAI API key with access to `gpt-4o`.

### Frontend (`frontend/.env`)
*   `NEXT_PUBLIC_API_URL`: The fully qualified URL to the deployed backend (e.g., `https://api.novax.ai` or `http://localhost:8000`).

## 2. Database Management
NOVA X uses Alembic for database migrations. 
*   **Generate Migration**: `alembic revision --autogenerate -m "Message"`
*   **Apply Migration**: `alembic upgrade head`
*   **Stamp DB**: If running against a pre-existing schema without alembic history, run `alembic stamp head`.

## 3. Seeding Demo Data
For Hackathon presentations or testing, a mock user and populated project can be seeded into the database via a Python script.
1. Ensure the DB is empty or at least missing the user `demo@novax.ai`.
2. Run `python seed_demo_data.py`.
3. The platform can now be accessed via the UI by clicking "Demo Mode".

## 4. Deployment Strategies
*   **Docker Compose**: Excellent for self-hosted instances. Runs Next.js in standalone mode and Uvicorn on 0.0.0.0.
*   **PaaS (Vercel/Render)**: Recommended for zero-maintenance hackathon deploys. Connect the Vercel project to `frontend/` and Render web service to `backend/`.
