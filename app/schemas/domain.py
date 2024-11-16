from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class Config:
    arbitrary_types_allowed = True


class FallacyType(str, Enum):
    AD_HOMINEM = "ad_hominem"
    STRAW_MAN = "straw_man"
    FALSE_DICHOTOMY = "false_dichotomy"
    SLIPPERY_SLOPE = "slippery_slope"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    HASTY_GENERALIZATION = "hasty_generalization"
    CIRCULAR_REASONING = "circular_reasoning"
    APPEAL_TO_EMOTION = "appeal_to_emotion"
    RED_HERRING = "red_herring"
    BANDWAGON = "bandwagon"
    FALSE_CAUSE = "false_cause"
    APPEAL_TO_TRADITION = "appeal_to_tradition"
    TU_QUOQUE = "tu_quoque"
    NO_TRUE_SCOTSMAN = "no_true_scotsman"


class TextSpan(BaseModel):
    start: int = Field(..., description="該当テキストの開始位置")
    end: int = Field(..., description="該当テキストの終了位置")

    class Config:
        arbitrary_types_allowed = True


class FallacyTypeDetail(BaseModel):
    type: FallacyType = Field(..., description="詭弁の種類")
    confidence: float = Field(..., description="この詭弁タイプの確信度(0~1)")
    explanation: str = Field(..., description="なぜこの詭弁に該当するかの説明")
    relevant_text: str = Field(..., description="入力文字列中の該当箇所")
    text_span: TextSpan

    class Config:
        arbitrary_types_allowed = True


class Metadata(BaseModel):
    analysis_timestamp: datetime = Field(default_factory=datetime.now)
    llm_version: str = Field(..., description="使用したLLMのバージョン")

    class Config:
        arbitrary_types_allowed = True


class FallacyAnalysis(BaseModel):
    """AIによる詭弁判定の結果"""

    input: str = Field(..., description="分析対象の文字列")
    is_fallacy: bool = Field(..., description="詭弁かどうかの判定結果")
    confidence_score: float = Field(..., description="判定の確信度(0~1)")
    fallacy_types: List[FallacyTypeDetail] = Field(default_factory=list)


class FallacyAnalysisWithMetadata(BaseModel):
    """ドメインモデル"""

    input: str = Field(..., description="分析対象の文字列")
    is_fallacy: bool = Field(..., description="詭弁かどうかの判定結果")
    confidence_score: float = Field(..., description="判定の確信度(0~1)")
    fallacy_types: List[FallacyTypeDetail] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    llm_version: str = Field(..., description="使用したLLMのバージョン")

    class Config:
        arbitrary_types_allowed = True
