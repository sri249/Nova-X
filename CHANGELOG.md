# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-06

### Added
- **Core Engine:** Fully functional multi-step Startup Generation Wizard.
- **AI Integration:** Integration with LangChain and OpenAI `gpt-4o-mini` with structured Pydantic outputs.
- **AI Modules:** Problem Discovery, Innovation DNA, Startup Formation, Market Intelligence, Financial Planner, Startup Health, AI Mentor, Risk Engine, Investor Hub, Task Planner.
- **Mock Fallback:** Fallback Mock AI generation for seamless execution without OpenAI credentials.
- **Auth:** Complete JWT-based authentication system with route guards.
- **Demo Mode:** Quick-access demo accounts and pre-seeded database.
- **Database:** Fully async SQLAlchemy 2.0 implementation over Neon PostgreSQL.
- **Frontend UI:** Responsive Tailwind CSS styling with dynamic Next.js App Router navigation.
- **Error Handling:** Global Next.js error boundaries and resilient Axios interceptors.

### Changed
- Refactored `DashboardPage` to guarantee type-safety on all list renders.
- Standardized `AIMetadata` injection across all mock services to guarantee Pydantic validation passes.
- Re-architected Sidebar navigation and nested routing for deep project links.

### Fixed
- Fixed 404 routing errors on the `/projects` page.
- Fixed `MarketIntelligenceOutput` 500 internal server error triggered by missing metadata keys in fallback mode.
- Fixed silent frontend crashes by implementing explicit API error states on the dashboard.
- Removed unused dependencies and cleaned up imports for production build.

### Security
- Enforced strict dependency injection for all protected FastAPI routes using `get_current_user`.
- Passwords fully secured using `passlib` with bcrypt hashing.
- Standardized CORS middleware for explicit frontend origins.
