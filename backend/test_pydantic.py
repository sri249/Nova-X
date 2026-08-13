from pydantic import BaseModel


class AIMetadata(BaseModel):
    confidence_score: int
    sources_or_assumptions: list[str]
    model_version: str
    generated_at: str

class InvestorHubOutput(BaseModel):
    executive_summary: str
    ai_metadata: AIMetadata

output = InvestorHubOutput(
    executive_summary="test",
    ai_metadata={"confidence_score": 90, "sources_or_assumptions": ["Mock"], "model_version": "mock", "generated_at": ""}
)

print(type(output.ai_metadata))
print(output.ai_metadata.model_dump())
