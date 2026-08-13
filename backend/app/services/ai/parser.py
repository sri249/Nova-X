from pydantic import BaseModel, Field


class AIMetadata(BaseModel):
    confidence_score: int = Field(description="Confidence score from 0 to 100 for the generated response.")
    sources_or_assumptions: list[str] = Field(description="List of assumed variables or simulated sources.")
    model_version: str = Field(description="The AI model version used for generation (e.g. gpt-4o).")
    generated_at: str = Field(description="ISO timestamp of when this was generated.")

class ProblemDiscoveryOutput(BaseModel):
    problem_summary: str = Field(description="A clear, concise summary of the problem.")
    root_cause_analysis: dict = Field(description="A JSON object mapping root causes to their descriptions.")
    stakeholders: list[str] = Field(description="List of stakeholders impacted by the problem.")
    impact_analysis: dict = Field(description="A JSON object describing the qualitative and quantitative impact.")
    opportunity_score: int = Field(description="A score from 0 to 100 indicating the startup opportunity size.")
    sdg_alignment: list[str] = Field(description="List of UN Sustainable Development Goals this problem aligns with.")
    key_insights: list[str] = Field(description="Key non-obvious insights regarding the problem space.")

class InnovationDNAOutput(BaseModel):
    innovation_score: int = Field(description="A score from 0 to 100 for overall innovation.")
    originality_score: int = Field(description="A score from 0 to 100 for originality.")
    competitor_overview: list[str] = Field(description="List of existing competitors and their approaches.")
    market_gap: str = Field(description="Description of the unfulfilled market gap.")
    novelty_analysis: str = Field(description="Analysis of why this specific approach is novel.")
    differentiation: list[str] = Field(description="Key differentiators against existing solutions.")
    patent_potential_indicator: str = Field(description="Informational assessment of patentability ('High', 'Medium', 'Low').")
    innovation_radar_visualization: dict = Field(description="Data points for an innovation radar chart (keys: technology, market, business_model, process, product). Values between 0-100.")

class StartupFormationOutput(BaseModel):
    startup_name: str
    tagline: str
    mission: str
    vision: str
    core_values: list[str]
    brand_personality: str
    logo_prompt: str
    color_palette: list[str] = Field(description="List of 3 to 5 hex codes.")
    customer_persona: dict = Field(description="Keys: age, occupation, income, demographics, psychographics, goals, pain points.")
    value_proposition: str
    unique_selling_proposition: str
    elevator_pitch: str
    business_model_canvas: dict = Field(description="Keys: key_partners, key_activities, key_resources, value_propositions, customer_relationships, channels, customer_segments, cost_structure, revenue_streams.")
    revenue_model: dict = Field(description="Details on how the startup makes money. Keys: model_type, pricing, lifetime_value, acquisition_cost")
    pricing_strategy: str
    swot_analysis: dict = Field(description="Keys: strengths, weaknesses, opportunities, threats.")
    product_roadmap: list[dict] = Field(description="List of milestones with keys: title, description, timeline (e.g. Q1 2027)")
    launch_checklist: list[str]

class MarketIntelligenceOutput(BaseModel):
    tam_sam_som: dict = Field(description="Keys: TAM, SAM, SOM with estimated dollar values and descriptions.")
    industry_growth_rate: str
    cagr: str
    market_maturity: str
    customer_personas: list[dict] = Field(description="Detailed customer segments.")
    adoption_curve: str
    seasonal_trends: str
    market_trends: list[str]
    geographic_expansion: list[str]
    regulatory_risks: list[str]
    emerging_technologies: list[str]
    swot_analysis: dict = Field(description="Keys: strengths, weaknesses, opportunities, threats.")
    competitor_matrix: list[dict] = Field(description="List of competitors with keys: name, product, pricing, strengths, weaknesses, market_position, target_customers, funding_stage, differentiation.")
    market_gap_analysis: str
    barriers_to_entry: list[str]
    market_readiness_score: int = Field(description="Score 0-100.")
    ai_metadata: AIMetadata

class FinancialPlannerOutput(BaseModel):
    startup_costs: dict = Field(description="Breakdown of initial costs (keys: category, amount, description).")
    monthly_operating_costs: dict = Field(description="Breakdown of recurring costs.")
    hiring_costs: dict = Field(description="Estimated personnel costs.")
    marketing_budget: dict = Field(description="Marketing and acquisition costs.")
    infrastructure_cost: dict = Field(description="Tech and physical infrastructure.")
    revenue_forecast: list[dict] = Field(description="List of monthly/yearly projections. Keys: period, revenue, expenses, profit.")
    cash_flow: list[dict] = Field(description="Monthly cash flow projection.")
    burn_rate: str
    runway: str = Field(description="Estimated runway in months based on current funding requirement.")
    break_even_month: str = Field(description="Month/Year when the startup becomes profitable.")
    funding_requirement: str = Field(description="Total funding needed to reach profitability.")
    funding_recommendation: str = Field(description="Recommended funding strategy (e.g. Seed, Bootstrapped).")
    roi_projection: str
    ai_metadata: AIMetadata

class StartupHealthOutput(BaseModel):
    innovation_score: int = Field(description="0-100")
    market_score: int = Field(description="0-100")
    business_score: int = Field(description="0-100")
    financial_score: int = Field(description="0-100")
    technology_score: int = Field(description="0-100")
    scalability_score: int = Field(description="0-100")
    execution_score: int = Field(description="0-100")
    investment_readiness: int = Field(description="0-100")
    overall_health_score: int = Field(description="0-100 aggregate score")
    ai_recommendations: dict = Field(description="Detailed recommendations. Keys: critical_risks, immediate_actions, long_term_strategy")
    ai_metadata: AIMetadata

class InvestorHubOutput(BaseModel):
    executive_summary: str = Field(description="A compelling 1-2 paragraph executive summary.")
    investment_memo: str = Field(description="A detailed memo simulating a VC partner's investment thesis.")
    funding_strategy: str = Field(description="Strategic advice on raising capital (stages, amounts, target investors).")
    one_page_profile: dict = Field(description="Keys: vision, problem, solution, traction, market, team, ask.")
    due_diligence_checklist: list[str] = Field(description="Checklist for VC due diligence.")
    milestone_roadmap: list[dict] = Field(description="Keys: milestone, timeframe, required_capital.")
    pitch_deck: dict = Field(description="Structured Pitch Deck. Keys must include: problem, solution, market, business_model, competition, traction, financials, roadmap, funding_ask, team. Each key should map to an object with 'title', 'subtitle', and 'bullet_points' (list of strings).")
    ai_metadata: AIMetadata

class RiskProfileOutput(BaseModel):
    technical_risks: list[dict] = Field(description="Keys: risk, level (High/Medium/Low), impact, probability, mitigation_plan.")
    market_risks: list[dict] = Field(description="Keys: risk, level, impact, probability, mitigation_plan.")
    financial_risks: list[dict] = Field(description="Keys: risk, level, impact, probability, mitigation_plan.")
    legal_risks: list[dict] = Field(description="Keys: risk, level, impact, probability, mitigation_plan.")
    execution_risks: list[dict] = Field(description="Keys: risk, level, impact, probability, mitigation_plan.")
    hiring_risks: list[dict] = Field(description="Keys: risk, level, impact, probability, mitigation_plan.")
    ai_metadata: AIMetadata

class TaskPlannerOutput(BaseModel):
    immediate_tasks: list[dict] = Field(description="Keys: task, description, priority (High/Medium/Low), status (Pending).")
    day_30_plan: list[dict] = Field(description="Keys: task, description, priority, status.")
    day_90_plan: list[dict] = Field(description="Keys: task, description, priority, status.")
    month_6_plan: list[dict] = Field(description="Keys: task, description, priority, status.")
    fundraising_timeline: list[dict] = Field(description="Keys: phase, timeline, objectives.")
    product_timeline: list[dict] = Field(description="Keys: phase, timeline, objectives.")
    ai_metadata: AIMetadata

class AIMentorOutput(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    missing_information: list[str] = Field(description="Critical blindspots the user needs to figure out.")
    risk_alerts: list[dict] = Field(description="Keys: level (High/Medium/Low), alert (string).")
    recommended_next_actions: list[dict] = Field(description="Keys: action, priority (High/Medium/Low).")
    weekly_priorities: list[str]
    ai_metadata: AIMetadata
