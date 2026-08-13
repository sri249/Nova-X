# NOVA X - AI-Powered Startup Incubator

NOVA X is a comprehensive AI-driven platform that acts as a virtual Co-Founder, guiding entrepreneurs from idea conception to pitch-ready presentation. Built for speed, precision, and robust analytical insight.

## Features
- **Problem Discovery:** Map core problems, perform root cause analysis, and measure impact.
- **Innovation DNA:** Define unique value propositions and track market gaps using AI.
- **Startup Formation:** Generate mission statements, logos, and comprehensive roadmaps.
- **Market Intelligence:** Analyze TAM/SAM/SOM, market trends, and perform automated SWOT analysis.
- **Financial Planner:** Predict burn rates, runway, break-even months, and funding requirements.
- **AI Co-Founder (Chat):** Context-aware persistent AI mentorship spanning across the entire project lifecycle.
- **Investor Hub & Export:** Generate one-page profiles, investment memos, and fully constructed Pitch Deck JSONs.
- **Dashboard & Analytics:** A modern, dark-mode ready dashboard leveraging Tremor/Recharts for Startup Health, Risk, and Financial visualizations.

## Technology Stack
- **Frontend**: Next.js 16 (App Router), React, Tailwind CSS 4, Shadcn/ui.
- **Backend**: FastAPI, Python 3.11+, SQLAlchemy 2.0 (Async), Alembic.
- **Database**: PostgreSQL (Neon DB).
- **AI Integration**: OpenAI (GPT-4o), LangChain, LangGraph.

## Installation & Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/novax.git
   cd novax
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Setup .env with DATABASE_URL, SECRET_KEY, and OPENAI_API_KEY
   
   # Run migrations & seed demo data
   alembic upgrade head
   python seed_demo_data.py
   
   # Start Server
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   
   # Create .env with NEXT_PUBLIC_API_URL=http://localhost:8000
   
   # Start Client
   npm run dev
   ```

## Deployment
NOVA X is fully containerized. Use `docker-compose up --build -d` for a single-command deployment, or deploy the frontend to **Vercel** and the backend to **Render** independently.


## Architecture
See `docs/ARCHITECTURE.md` and `docs/SYSTEM_DIAGRAM.md` for a comprehensive breakdown of the application flow, data models, and API interactions.
