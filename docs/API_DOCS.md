# NOVA X - API Documentation

Base URL: `http://localhost:8000/api`

## Authentication (`/auth`)
All subsequent endpoints require a Bearer token received from these endpoints.
- `POST /register`: Registers a new user. Expects `email`, `password`, `full_name`.
- `POST /login`: Authenticates user. Expects `email`, `password`. Returns `access_token`.

## Project Management (`/projects`)
**Headers**: `Authorization: Bearer <token>`
- `GET /`: Lists all projects for the authenticated user.
- `POST /`: Creates a new project.
- `GET /{id}`: Retrieves comprehensive project details (including related AI modules).

## AI Modules
**Headers**: `Authorization: Bearer <token>`
These endpoints accept project context, pass it to OpenAI, and return structured JSON.
- `POST /{id}/problem-discovery`: Analyzes the core problem space.
- `POST /{id}/innovation-dna`: Determines unfair advantages and UVPs.
- `POST /{id}/startup-formation`: Generates branding, names, and roadmaps.
- `POST /{id}/market-intelligence`: Generates TAM/SAM/SOM and SWOT analysis.
- `POST /{id}/financial-planner`: Projects runway and funding requirements.

## Chat (`/chat`)
**Headers**: `Authorization: Bearer <token>`
- `POST /{project_id}/message`: Sends a message to the AI Co-Founder. Context-aware based on the project's current generated modules.

## Export (`/export`)
**Headers**: `Authorization: Bearer <token>`
- `GET /{project_id}/pdf`: Returns a formatted HTML document designed for print-to-PDF functionality.
- `GET /{project_id}/pitch-deck`: Returns a JSON representation of the startup formatted as a 5-slide pitch deck.
