from typing import List
from pydantic import BaseModel, Field
from app.schemas.domain import (
    FallacyAnalysisWithMetadata,
    FallacyTypeDetail,
    Metadata,
    FallacyAnalysis,
)


class JudgeResponse(BaseModel):
    input: str = Field(..., description="分析対象の文字列")
    is_fallacy: bool = Field(..., description="詭弁かどうかの判定結果")
    confidence_score: float = Field(..., ge=0, le=1, description="判定の確信度")
    fallacy_types: List[FallacyTypeDetail] = Field(default_factory=list)
    metadata: Metadata

    @classmethod
    def from_domain(cls, analysis: FallacyAnalysisWithMetadata) -> "JudgeResponse":
        """ドメインモデルからレスポンスモデルへの変換"""
        return cls(
            input=analysis.input,
            is_fallacy=analysis.is_fallacy,
            confidence_score=analysis.confidence_score,
            fallacy_types=analysis.fallacy_types,
            metadata=Metadata(
                analysis_timestamp=analysis.timestamp,
                llm_version=analysis.llm_version,
            ),
        )
