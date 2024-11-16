from app.schemas.domain import FallacyAnalysis, FallacyType, FallacyTypeDetail
from app.services.llm import AgentOpenAI


class FallacyAnalyzer:
    def __init__(
        self,
    ):
        self.agent = AgentOpenAI("gpt-4o-mini")

    async def judge(self, text: str, language: str) -> FallacyAnalysis:
        """詭弁判定を行う"""
        return await self.agent.judge(text, language)
