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

    HYPOTHETICAL_FALLACY = "hypothetical_fallacy"  # 仮定による詭弁
    RARE_EXCEPTION = "rare_exception"  # 例外による詭弁
    FUTURE_PREDICTION = "future_prediction"  # 未来予測による詭弁
    SUBJECTIVE_ASSUMPTION = "subjective_assumption"  # 主観的決めつけ
    UNSUPPORTED_CONSENSUS = "unsupported_consensus"  # 根拠なき一般論
    CONSPIRACY_THEORY = "conspiracy_theory"  # 陰謀論
    PERSONAL_ATTACK = "personal_attack"  # 人格攻撃
    IMPOSSIBLE_SOLUTION = "impossible_solution"  # 実現不可能な解決策
    LABELING = "labeling"  # レッテル貼り
    IGNORING_SETTLEMENT = "ignoring_settlement"  # 既決事項の無視
    FALSE_VICTORY = "false_victory"  # 虚偽の勝利宣言
    NITPICKING = "nitpicking"  # 細部の誤りの指摘
    PROGRESS_FALLACY = "progress_fallacy"  # 進歩による正当化
    BLACK_AND_WHITE = "black_and_white"  # 二者択一的思考
    EXTREME_EXTRAPOLATION = "extreme_extrapolation"  # 極論化
    TOPIC_DIVERSION = "topic_diversion"  # 話題のすり替え
    AUTHORITY_DISMISSAL = "authority_dismissal"  # 権威による否定


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
