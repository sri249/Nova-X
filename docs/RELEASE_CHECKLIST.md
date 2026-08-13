# NOVA X - Release Checklist

Ensure these items are ticked before declaring the release final.

## 1. Local Verification
- [x] Backend runs locally (`uvicorn`).
- [x] Frontend runs locally (`npm run dev`).
- [x] `test_workflow.py` completes 100% of integration checks.
- [x] `seed_demo_data.py` completes successfully.

## 2. Docker Validation
- [x] `docker-compose build` succeeds.
- [x] Frontend `Dockerfile` utilizes `output: standalone`.

## 3. Database (Neon PostgreSQL)
- [x] Remote DB is active.
- [x] `alembic upgrade head` executed successfully against remote DB.
- [x] `seed_demo_data.py` executed successfully against remote DB.

## 4. Backend Deployment (Render)
- [x] Environment variable `DATABASE_URL` is set.
- [x] Environment variable `SECRET_KEY` is set.
- [x] Environment variable `OPENAI_API_KEY` is set.
- [x] Build script: `pip install -r requirements.txt`.
- [x] Start script: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

## 5. Frontend Deployment (Vercel)
- [x] Environment variable `NEXT_PUBLIC_API_URL` points to the Render URL.
- [x] Vercel build command: `npm run build` succeeds without TS errors.

## 6. Functional End-to-End
- [x] Demo User (`demo@novax.ai`) successfully logs in.
- [x] Demo User sees fully populated project data.
- [x] Demo User can chat with the AI Co-Founder.
- [x] Demo User can export Pitch Deck JSON.
