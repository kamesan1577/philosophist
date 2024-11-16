import json
from app.schemas.domain import (
    FallacyAnalysis,
    FallacyAnalysisWithMetadata,
    FallacyType,
    FallacyTypeDetail,
)
from app.services.llm import AgentOpenAI
from app.infrastructure.redis_client import RedisClient
from datetime import datetime


class FallacyAnalyzer:
    def __init__(
        self,
        model: str = "gpt-4o-mini",
    ):
        self.agent = AgentOpenAI(model)
        self.redis_client = RedisClient()

    async def judge(self, text: str, language: str) -> FallacyAnalysis:
        """詭弁判定を行う"""
        cache_key = f"{self.agent.model}:{text}"
        cached_response = self.redis_client.get(cache_key)
        if cached_response:
            return FallacyAnalysisWithMetadata(**json.loads(cached_response))

        analysis_result = await self.agent.judge(text, language)
        analysis_result_dict = analysis_result.model_dump()

        # datetimeオブジェクトを文字列に変換
        for key, value in analysis_result_dict.items():
            if isinstance(value, datetime):
                analysis_result_dict[key] = value.isoformat()

        self.redis_client.set(cache_key, json.dumps(analysis_result_dict))
        return analysis_result
