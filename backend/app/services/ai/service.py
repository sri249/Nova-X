from datetime import datetime, timezone

from langchain_openai import ChatOpenAI

from app.core.config import settings

from .parser import (
    AIMentorOutput,
    FinancialPlannerOutput,
    InnovationDNAOutput,
    InvestorHubOutput,
    MarketIntelligenceOutput,
    ProblemDiscoveryOutput,
    RiskProfileOutput,
    StartupFormationOutput,
    StartupHealthOutput,
    TaskPlannerOutput,
)
from .prompt_manager import PromptManager


class AIService:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.mock_mode = not bool(self.api_key)
        if not self.mock_mode:
            self.llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini", api_key=self.api_key)
        else:
            self.llm = None

    @staticmethod
    def _metadata() -> dict:
        return {
            "confidence_score": 72,
            "sources_or_assumptions": ["Demo estimate based on the project context; validate with customer research."],
            "model_version": "contextual-demo-v1",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _topic(context: object) -> str:
        text = str(context or "startup").replace("\n", " ")
        return text[:140] if text else "startup"

    async def generate_problem_discovery(self, inputs: dict) -> ProblemDiscoveryOutput:
        if self.mock_mode:
            return ProblemDiscoveryOutput(
                problem_summary=f"{inputs.get('title', 'The startup')} addresses a decision gap: {inputs.get('description', 'customers lack timely, practical guidance.')}",
                root_cause_analysis={"Fragmented information": "Users must reconcile disconnected sources before making time-sensitive decisions.", "Lack of personalization": f"Available advice is generic and does not reflect the needs of {inputs.get('target_users', 'the intended users')}.", "Delayed action": "Insights arrive after the decision window, reducing their operational value."},
                stakeholders=[inputs.get('target_users', 'Primary users'), "Operators and advisors", "Partners who depend on better outcomes"],
                impact_analysis={"social": "Users lose confidence when they cannot act on reliable guidance.", "economic": "Poor decisions create avoidable cost, lost revenue, and wasted time.", "environmental": "Better recommendations can reduce unnecessary resource use."},
                opportunity_score=85,
                sdg_alignment=["No Poverty", "Zero Hunger"],
                key_insights=[f"{inputs.get('title', 'This startup')} should begin with one high-frequency decision workflow.", "Trust improves when every recommendation explains the underlying signal and next action."]
            )
        
        prompt = PromptManager.get_problem_discovery_prompt()
        chain = prompt | self.llm.with_structured_output(ProblemDiscoveryOutput)
        return await chain.ainvoke(inputs)

    async def generate_innovation_dna(self, problem_summary: str, root_causes: dict) -> InnovationDNAOutput:
        if self.mock_mode:
            return InnovationDNAOutput(
                innovation_score=82, originality_score=78, competitor_overview=["Point solutions", "Manual advisory services", "Generic workflow software"],
                market_gap=f"Existing alternatives do not turn {self._topic(problem_summary)} into one prioritized, actionable workflow.", novelty_analysis="The opportunity is to combine fragmented signals with transparent, role-specific recommendations rather than another standalone data source.",
                differentiation=["A single decision workflow that combines fragmented inputs.", "Recommendations explain why an action matters and what to do next.", "A feedback loop that improves guidance from user outcomes."], patent_potential_indicator="Medium",
                innovation_radar_visualization={"technology": 82, "market": 76, "business_model": 74, "process": 78, "product": 84}
            )

        prompt = PromptManager.get_innovation_dna_prompt()
        chain = prompt | self.llm.with_structured_output(InnovationDNAOutput)
        return await chain.ainvoke({"problem_summary": problem_summary, "root_causes": root_causes})

    async def generate_startup_formation(self, problem_data: str, innovation_data: str) -> StartupFormationOutput:
        if self.mock_mode:
            return StartupFormationOutput(
                startup_name="DecisionFlow AI", tagline="Clarity for every critical decision.", mission="Make expert-quality operational guidance accessible at the moment it is needed.", vision="A world where smaller teams can act with the confidence of a specialist.",
                core_values=["Customer evidence", "Practical clarity", "Responsible automation"], brand_personality="Clear, dependable, and pragmatic", logo_prompt="A clean compass mark formed from connected data points in deep green and blue.",
                color_palette=["#0F766E", "#2563EB", "#F8FAFC"], customer_persona={"age": "30-55", "occupation": "Owner or operating manager", "goals": ["Make faster, higher-quality decisions"], "pain_points": ["Fragmented information", "Limited specialist support"]},
                value_proposition=f"Convert {self._topic(problem_data)} into prioritized, explainable next actions.", unique_selling_proposition=f"Combines the problem context with a transparent recommendation workflow: {self._topic(innovation_data)}", elevator_pitch="DecisionFlow AI gives operators one place to turn scattered information into clear, timely decisions and measurable next steps.",
                business_model_canvas={"customer_segments": "Small and medium operating teams", "channels": ["Industry partners", "Direct sales"], "value_propositions": "Actionable recommendations", "revenue_streams": "Subscription and partner plans"}, revenue_model={"model_type": "SaaS subscription", "pricing": "Tiered monthly plans", "lifetime_value": "Driven by retained operational value", "acquisition_cost": "Partner-led and direct sales"},
                pricing_strategy="Start with a paid pilot, then offer tiered subscriptions by active workflow.", swot_analysis={"strengths": ["Clear decision workflow"], "weaknesses": ["Requires trusted input data"], "opportunities": ["Partner distribution"], "threats": ["Incumbent feature expansion"]},
                product_roadmap=[{"title": "Pilot workflow", "description": "Validate one urgent customer decision", "timeline": "First 90 days"}], launch_checklist=["Interview ten target users and define the pilot success metric."]
            )

        prompt = PromptManager.get_startup_formation_prompt()
        chain = prompt | self.llm.with_structured_output(StartupFormationOutput)
        return await chain.ainvoke({"problem_data": problem_data, "innovation_data": innovation_data})

    async def generate_market_intelligence(self, context: str) -> MarketIntelligenceOutput:
        if self.mock_mode:
            return MarketIntelligenceOutput(
                tam_sam_som={"TAM": "Demo estimate: ₹8,000 crore addressable workflow market", "SAM": "Demo estimate: ₹900 crore initial segment", "SOM": "Demo estimate: ₹45 crore achievable beachhead"}, industry_growth_rate="Demo estimate: 14% annual growth", cagr="Demo estimate: 14%", market_maturity="Growing",
                customer_personas=[{"name": "Operational decision maker", "need": "Reliable next-step guidance"}], adoption_curve="Early adopters who already feel the cost of fragmented decisions", seasonal_trends="Demand rises around planning and high-risk operational periods", market_trends=["Decision-support automation", "Explainable AI", "Vertical workflow software"], geographic_expansion=["Begin in the project’s primary market, then expand through channel partners"], regulatory_risks=["Validate sector-specific data and advisory requirements"],
                emerging_technologies=["Explainable machine learning", "Workflow automation"], swot_analysis={"strengths": ["Clear customer pain"], "weaknesses": ["Early proof required"], "opportunities": ["Partner distribution"], "threats": ["Incumbents"]}, competitor_matrix=[{"name": "Manual process", "strengths": "Familiar", "weaknesses": "Slow and inconsistent"}, {"name": "Point tools", "strengths": "Focused data", "weaknesses": "No end-to-end decision workflow"}], market_gap_analysis=f"The market lacks a trusted workflow that converts {self._topic(context)} into timely, explainable action.",
                barriers_to_entry=["Build customer trust through measurable pilot outcomes", "Secure high-quality workflow inputs"], market_readiness_score=78, ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_market_intelligence_prompt()
        chain = prompt | self.llm.with_structured_output(MarketIntelligenceOutput)
        return await chain.ainvoke({"context": context})

    async def generate_financial_planner(self, context: str, market_data: str) -> FinancialPlannerOutput:
        if self.mock_mode:
            return FinancialPlannerOutput(
                startup_costs={"product_validation": "₹6,00,000", "initial_setup": "₹2,00,000"}, monthly_operating_costs={"product_and_data": "₹2,50,000", "customer_success": "₹1,25,000", "operations": "₹75,000"}, hiring_costs={"lean_team": "₹4,50,000 per month"}, marketing_budget={"pilot_acquisition": "₹75,000 per month"}, infrastructure_cost={"cloud_and_tools": "₹60,000 per month"},
                revenue_forecast=[{"period": "Year 1", "revenue": "₹30,00,000", "expenses": "₹54,00,000", "profit": "-₹24,00,000"}, {"period": "Year 2", "revenue": "₹1,20,00,000", "expenses": "₹90,00,000", "profit": "₹30,00,000"}], cash_flow=[{"period": "Months 1-6", "net_cash_flow": "-₹27,00,000"}, {"period": "Months 7-12", "net_cash_flow": "-₹18,00,000"}], burn_rate="₹4,50,000/month", runway="18 months with ₹81,00,000 available", break_even_month="Month 18", funding_requirement="₹1.2 crore", funding_recommendation="Raise a seed round after proving paid pilot retention", roi_projection="Demo estimate: 3x revenue potential by year three", ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_financial_planner_prompt()
        chain = prompt | self.llm.with_structured_output(FinancialPlannerOutput)
        return await chain.ainvoke({"context": context, "market_data": market_data})

    async def generate_startup_health(self, context: str, financial_data: str, market_data: str) -> StartupHealthOutput:
        if self.mock_mode:
            return StartupHealthOutput(
                innovation_score=85, market_score=90, business_score=80, financial_score=75, technology_score=88,
                scalability_score=82, execution_score=70, investment_readiness=85, overall_health_score=82,
                ai_recommendations={"critical_risks": ["Validate that target users will pay for the first workflow."], "immediate_actions": ["Run ten structured customer interviews and secure three paid pilots."], "long_term_strategy": ["Build a repeatable partner channel after measurable pilot results."]}, ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_startup_health_prompt()
        chain = prompt | self.llm.with_structured_output(StartupHealthOutput)
        return await chain.ainvoke({"context": context, "financial_data": financial_data, "market_data": market_data})

    async def regenerate_single_field(self, context: str, field_name: str, current_content: str) -> str:
        if self.mock_mode:
            return f"Refined {field_name}: {self._topic(context)}. Keep the recommendation specific, measurable, and tied to the customer’s next decision."
            
        prompt = PromptManager.get_single_field_regeneration_prompt()
        # Since it's returning a single string, we just use the default StrOutputParser (or just get the text)
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "context": context, 
            "field_name": field_name, 
            "current_content": current_content
        })
        return response.content

    async def generate_investor_hub(self, context: str) -> InvestorHubOutput:
        if self.mock_mode:
            return InvestorHubOutput(
                executive_summary=f"{self._topic(context)} is building an explainable decision-support workflow for an underserved operating problem.", investment_memo="Investment thesis: fund a focused pilot-led product that can demonstrate retention, measurable customer value, and channel scalability before expanding its workflow suite.", funding_strategy="Use a seed round to validate paid pilots, product reliability, and repeatable distribution.", one_page_profile={"vision": "Trusted decision support for every operating team", "problem": "Fragmented information delays high-value actions", "solution": "Explainable workflow recommendations", "ask": "Capital for pilots and product validation"}, due_diligence_checklist=["Pilot contracts and retention evidence", "Data-handling controls", "Unit-economics assumptions"], milestone_roadmap=[{"milestone": "Three paid pilots", "timeframe": "90 days", "required_capital": "₹25 lakh"}], pitch_deck={"problem": {"title": "Fragmented decisions", "subtitle": "Customers lack timely, trusted guidance", "bullet_points": ["High cost of delay", "Disconnected tools"]}, "solution": {"title": "One actionable workflow", "subtitle": "Explainable recommendations", "bullet_points": ["Prioritized next steps"]}}, ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_investor_hub_prompt()
        chain = prompt | self.llm.with_structured_output(InvestorHubOutput)
        return await chain.ainvoke({"context": context})

    async def generate_risk_profile(self, context: str) -> RiskProfileOutput:
        if self.mock_mode:
            return RiskProfileOutput(
                technical_risks=[{"risk": "Recommendations may be unreliable if inputs are incomplete", "level": "High", "impact": "Loss of customer trust", "probability": "Medium", "mitigation_plan": "Start with explainable rules and human review during pilots."}], market_risks=[{"risk": "Customers may retain existing manual workflows", "level": "High", "impact": "Slow adoption", "probability": "Medium", "mitigation_plan": "Sell a narrowly scoped paid pilot with a measurable outcome."}], financial_risks=[{"risk": "Pilot sales take longer than planned", "level": "Medium", "impact": "Higher burn", "probability": "Medium", "mitigation_plan": "Stage hiring and track weekly sales conversion."}], legal_risks=[{"risk": "Sector-specific guidance may require compliance review", "level": "Medium", "impact": "Launch delays", "probability": "Low", "mitigation_plan": "Validate obligations before making advisory claims."}], execution_risks=[{"risk": "Too many workflows dilute the initial product", "level": "High", "impact": "Weak product-market fit", "probability": "Medium", "mitigation_plan": "Commit to one high-frequency use case for the first release."}], hiring_risks=[{"risk": "Small team lacks domain credibility", "level": "Medium", "impact": "Lower trust", "probability": "Medium", "mitigation_plan": "Recruit an experienced domain advisor and pilot partners."}], ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_risk_engine_prompt()
        chain = prompt | self.llm.with_structured_output(RiskProfileOutput)
        return await chain.ainvoke({"context": context})

    async def generate_task_planner(self, context: str) -> TaskPlannerOutput:
        if self.mock_mode:
            return TaskPlannerOutput(
                immediate_tasks=[{"task": "Interview ten target users", "description": "Validate the highest-cost decision and willingness to pay.", "priority": "High", "status": "Pending"}], day_30_plan=[{"task": "Launch a concierge pilot", "description": "Deliver recommendations manually alongside the prototype.", "priority": "High", "status": "Pending"}], day_90_plan=[{"task": "Convert three paid pilots", "description": "Prove retention and a repeatable onboarding workflow.", "priority": "High", "status": "Pending"}], month_6_plan=[{"task": "Scale the validated workflow", "description": "Automate the most trusted parts of the pilot experience.", "priority": "Medium", "status": "Pending"}], fundraising_timeline=[{"phase": "Pilot evidence", "timeline": "0-3 months", "objectives": "Retention, value evidence, references"}], product_timeline=[{"phase": "Focused MVP", "timeline": "0-3 months", "objectives": "One explainable decision workflow"}], ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_task_planner_prompt()
        chain = prompt | self.llm.with_structured_output(TaskPlannerOutput)
        return await chain.ainvoke({"context": context})

    async def generate_ai_mentor(self, context: str) -> AIMentorOutput:
        if self.mock_mode:
            return AIMentorOutput(
                strengths=["The project targets a real, repeatable decision problem.", "A focused workflow can demonstrate value quickly."], weaknesses=["Customer willingness to pay is not yet proven.", "Input quality and trust must be earned."], missing_information=["Which single decision users make most often", "What outcome they will pay to improve"], risk_alerts=[{"level": "High", "alert": "Avoid expanding beyond the first validated workflow before pilot retention is proven."}], recommended_next_actions=[{"action": "Secure three design partners and measure one customer outcome weekly.", "priority": "High"}], weekly_priorities=["Conduct customer interviews", "Define the pilot success metric", "Review evidence with a domain advisor"], ai_metadata=self._metadata()
            )
        prompt = PromptManager.get_ai_mentor_prompt()
        chain = prompt | self.llm.with_structured_output(AIMentorOutput)
        return await chain.ainvoke({"context": context})

    async def generate_co_founder_chat(self, context: str, messages: list) -> str:
        if self.mock_mode:
            question = messages[-1].get("content", "your question") if messages else "your question"
            return f"For this project, the biggest near-term risk is proving that users will consistently act on and pay for the recommendation workflow. Your question was: '{question}'. Run a tightly scoped paid pilot, measure the decision outcome it improves, and use those results before expanding features."
        
        prompt = PromptManager.get_co_founder_chat_prompt()
        chain = prompt | self.llm
        response = await chain.ainvoke({
            "context": context,
            "messages": messages
        })
        return response.content

ai_service = AIService()
