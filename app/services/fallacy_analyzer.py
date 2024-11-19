import json
from typing import Optional
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
        model: str = "gpt-4o",
    ):
        self.agent = AgentOpenAI(model)
        self.redis_client = RedisClient()

    def _get_from_cache(self, cache_key: str) -> Optional[FallacyAnalysisWithMetadata]:
        """キャッシュからデータを取得する"""
        try:
            cached_response = self.redis_client.get(cache_key)
            if cached_response:
                return FallacyAnalysisWithMetadata(**json.loads(cached_response))
        except Exception as e:
            print(f"Cache retrieval error: {str(e)}")
        return None

    def _save_to_cache(self, cache_key: str, analysis_result: FallacyAnalysis) -> None:
        """結果をキャッシュに保存する"""
        try:
            analysis_result_dict = analysis_result.model_dump()

            # datetimeオブジェクトを文字列に変換
            for key, value in analysis_result_dict.items():
                if isinstance(value, datetime):
                    analysis_result_dict[key] = value.isoformat()

            self.redis_client.set(cache_key, json.dumps(analysis_result_dict))
        except Exception as e:
            print(f"Cache storage error: {str(e)}")

    async def judge(self, text: str, language: str) -> FallacyAnalysis:
        """詭弁判定を行う"""
        cache_key = f"{self.agent.model}:{text}"

        # キャッシュチェック
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result

        # 新規分析実行
        analysis_result = await self.agent.judge(text, language)

        # 結果をキャッシュに保存（非同期で実行するが失敗しても処理は継続）
        self._save_to_cache(cache_key, analysis_result)

        return analysis_result
