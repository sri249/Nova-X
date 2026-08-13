# NOVA X - Deployment Guide

This guide outlines the complete process for deploying NOVA X to production using modern serverless and PaaS providers.

## Architecture Overview
NOVA X is divided into three distinct layers:
1. **Frontend:** Next.js 14 App Router (Deployed on Vercel)
2. **Backend:** FastAPI (Deployed on Render / AWS ECS / Google Cloud Run)
3. **Database:** Neon Serverless PostgreSQL

## 1. Database Deployment (Neon)
1. Create an account at [Neon.tech](https://neon.tech).
2. Create a new Postgres project.
3. Copy the standard connection string (e.g. `postgresql://user:password@ep-cool-snowflake-123.us-east-2.aws.neon.tech/neondb`).
4. Replace `postgresql://` with `postgresql+asyncpg://` for compatibility with async SQLAlchemy.

## 2. Backend Deployment (Render)
1. Sign up for [Render.com](https://render.com).
2. Create a new **Web Service**.
3. Connect your GitHub repository containing the NOVA X code.
4. Set the Root Directory to `backend`.
5. Select **Docker** as the runtime environment.
6. Under **Environment Variables**, add:
   - `DATABASE_URL`: Your modified Neon connection string.
   - `SECRET_KEY`: A secure random string (e.g., generated via `openssl rand -hex 32`).
   - `OPENAI_API_KEY`: Your OpenAI API key (Optional. If omitted, the system falls back to mock data).
7. Under **Build Command / Start Command**, ensure Alembic runs before the server starts. You can configure a `render.yaml` or just let Docker handle it if the entrypoint is configured correctly.
8. Click **Deploy Web Service**. Render will build the Docker container and expose a public URL (e.g., `https://nova-api.onrender.com`).

## 3. Frontend Deployment (Vercel)
1. Sign up for [Vercel.com](https://vercel.com).
2. Create a new project and import the NOVA X GitHub repository.
3. Set the **Root Directory** to `frontend`.
4. The framework preset should automatically detect **Next.js**.
5. Under **Environment Variables**, add:
   - `NEXT_PUBLIC_API_URL`: The public URL of your deployed backend (e.g., `https://nova-api.onrender.com`).
6. Click **Deploy**. Vercel will build the frontend and provide a public URL.

## 4. Post-Deployment Verification
1. Navigate to your Vercel frontend URL.
2. Click **Try Demo** or Register a new account.
3. If the backend fails to connect, verify the `NEXT_PUBLIC_API_URL` environment variable matches exactly, with no trailing slashes.
4. If you get a 500 error during generation, ensure `OPENAI_API_KEY` is either valid or completely removed (to trigger fallback).

## Using Docker Compose (Local/VPS)
To deploy the entire stack on a single VPS (like DigitalOcean, AWS EC2, or Hetzner), simply clone the repo and run:
```bash
docker-compose up -d --build
```
Ensure you have created a `.env` file at the root containing the necessary variables.
