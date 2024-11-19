from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class Config:
    arbitrary_types_allowed = True


class FallacyType(str, Enum):
    AD_HOMINEM = "ad_hominem"  # 相手の人格や性質を攻撃することで議論を否定する論法
    STRAW_MAN = "straw_man"  # 相手の主張を歪曲して解釈し、それを批判する論法
    FALSE_DICHOTOMY = "false_dichotomy"  # 複数ある選択肢を二つに限定して議論する論法
    SLIPPERY_SLOPE = "slippery_slope"  # ある行為が連鎖的に悪い結果を招くと主張する論法
    APPEAL_TO_AUTHORITY = (
        "appeal_to_authority"  # 権威ある人や組織の意見を無批判に受け入れる論法
    )
    HASTY_GENERALIZATION = "hasty_generalization"  # 少数の事例から性急に一般化する論法
    CIRCULAR_REASONING = "circular_reasoning"  # 結論を前提として使用する循環論法
    APPEAL_TO_EMOTION = (
        "appeal_to_emotion"  # 感情に訴えかけることで論理的思考を妨げる論法
    )
    RED_HERRING = "red_herring"  # 議論の本質から外れた話題を持ち出して論点をずらす論法
    BANDWAGON = "bandwagon"  # 多数派の意見だからという理由で正当化する論法
    FALSE_CAUSE = (
        "false_cause"  # 因果関係のない事象を因果関係があるように結びつける論法
    )
    APPEAL_TO_TRADITION = (
        "appeal_to_tradition"  # 伝統的だからという理由で正当化する論法
    )
    TU_QUOQUE = (
        "tu_quoque"  # 「お前もやっている」と相手の非を指摘して自分の非を正当化する論法
    )
    NO_TRUE_SCOTSMAN = "no_true_scotsman"  # 反例を「本物ではない」と否定する論法

    HYPOTHETICAL_FALLACY = "hypothetical_fallacy"  # 仮定に基づいて現実を否定する論法
    RARE_EXCEPTION = "rare_exception"  # まれな例外を一般的な反例として扱う論法
    FUTURE_PREDICTION = (
        "future_prediction"  # 不確実な未来予測を確実なものとして扱う論法
    )
    SUBJECTIVE_ASSUMPTION = (
        "subjective_assumption"  # 主観的な判断を客観的事実として扱う論法
    )
    UNSUPPORTED_CONSENSUS = (
        "unsupported_consensus"  # 根拠のない一般的な認識を真実として扱う論法
    )
    CONSPIRACY_THEORY = (
        "conspiracy_theory"  # 陰謀があることを前提として事象を説明する論法
    )
    PERSONAL_ATTACK = "personal_attack"  # 個人を攻撃することで議論を否定する論法
    IMPOSSIBLE_SOLUTION = (
        "impossible_solution"  # 実現不可能な解決策を提示して議論を封じる論法
    )
    LABELING = "labeling"  # レッテル貼りによって相手を否定する論法
    IGNORING_SETTLEMENT = (
        "ignoring_settlement"  # 既に決着がついた事項を無視して議論を蒸し返す論法
    )
    FALSE_VICTORY = "false_victory"  # 勝利宣言によって議論を終わらせようとする論法
    NITPICKING = "nitpicking"  # 些細な誤りを指摘して全体を否定する論法
    PROGRESS_FALLACY = "progress_fallacy"  # 進歩や発展を理由に正当化する論法
    BLACK_AND_WHITE = "black_and_white"  # 事象を極端な二項対立で捉える論法
    EXTREME_EXTRAPOLATION = "extreme_extrapolation"  # 極端な例を用いて一般化する論法
    TOPIC_DIVERSION = "topic_diversion"  # 話題をずらして本質的な議論を避ける論法
    AUTHORITY_DISMISSAL = "authority_dismissal"  # 権威を否定することで議論を退ける論法

    ARGUMENT_FROM_IGNORANCE = (
        "argument_from_ignorance"  # 証明できないことを根拠に結論を導く論法
    )
    COMPOSITION_FALLACY = (
        "composition_fallacy"  # 部分の性質を全体の性質として一般化する論法
    )
    DIVISION_FALLACY = "division_fallacy"  # 全体の性質を部分の性質として適用する論法
    LOADED_LANGUAGE = (
        "loaded_language"  # 感情的な反応を引き出す言葉を使用して説得を試みる論法
    )
    COMPLEX_QUESTION = "complex_question"  # 複数の前提を含む質問で相手を困らせる論法
    APPEAL_TO_FORCE = "appeal_to_force"  # 力や脅威を用いて相手を説得しようとする論法
    CONTINUUM_FALLACY = (
        "continuum_fallacy"  # 境界が曖昧な概念を利用して論理を歪める論法
    )
    GOD_OF_GAPS = "god_of_gaps"  # 科学で説明できない現象を神の仕業とする論法
    NATURALISTIC_FALLACY = (
        "naturalistic_fallacy"  # 自然なことを善いことと同一視する論法
    )
    MORALISTIC_FALLACY = "moralistic_fallacy"  # 道徳的な「べき」から事実を否定する論法
    APPEAL_TO_PITY = "appeal_to_pity"  # 同情を引くことで論理的な議論を回避する論法
    APPEAL_TO_NOVELTY = "appeal_to_novelty"  # 新しいことを理由に正当化する論法
    GUILT_BY_ASSOCIATION = (
        "guilt_by_association"  # 関連する人や集団の否定的側面を理由に議論を否定する論法
    )
    CIRCUMSTANTIAL_AD_HOMINEM = (
        "circumstantial_ad_hominem"  # 相手の置かれた状況を理由に議論を否定する論法
    )
    IS_OUGHT_FALLACY = (
        "is_ought_fallacy"  # 事実から当為を導き出そうとする論法（ヒュームの法則）
    )


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
