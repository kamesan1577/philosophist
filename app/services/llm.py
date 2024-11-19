from abc import abstractmethod, ABC
import json
from openai import OpenAI

from app.schemas.domain import (
    FallacyAnalysis,
    FallacyAnalysisWithMetadata,
    FallacyType,
    FallacyTypeDetail,
)


class IAgent(ABC):

    @abstractmethod
    async def judge(self, text: str, language: str) -> FallacyAnalysis:
        raise NotImplementedError


class AgentOpenAI(IAgent):

    SYSTEM_PROMPT = """
次のメッセージで与えたテキストが詭弁かどうかを判定してください。

判定に使う入力は次のメッセージの内容のみであり、決して他の情報を使ってはいけません。
複数の詭弁が当てはまると考えた場合はすべてを出力結果に含めてください。
Inputにはどんな入力であろうと絶対に元の入力の忠実なコピーを入れてください。
TextSpanには該当する文言の開始位置と終了位置を示す。これらの位置は決して間違えてはならず、必ず正しい位置を返すように繰り返し確認を行うこと。

詭弁判定の参考として以下の定義を参照することが可能です。
    - AD_HOMINEM: 人身攻撃。相手の主張ではなく、人格や性格を攻撃する
    - STRAW_MAN: わら人形論法。相手の主張を歪曲して反論しやすい形に置き換える
    - FALSE_DICHOTOMY: 二分法の誤り。複数ある選択肢を意図的に二つに限定する
    - SLIPPERY_SLOPE: 滑りやすい坂。極端な結果を予測して反論する
    - APPEAL_TO_AUTHORITY: 権威への訴え。権威ある人物や組織の意見を無批判に受け入れる
    - HASTY_GENERALIZATION: 性急な一般化。不十分な証拠から一般的な結論を導く
    - CIRCULAR_REASONING: 循環論法。結論を前提として使用する
    - APPEAL_TO_EMOTION: 感情への訴え。論理の代わりに感情に訴える
    - RED_HERRING: 赤鯟。議論の本質からそらす
    - BANDWAGON: 流行への追従。多数派だからという理由で正当化する
    - FALSE_CAUSE: 偽りの因果関係。相関関係を因果関係と誤認する
    - APPEAL_TO_TRADITION: 伝統への訴え。長年の慣習という理由で正当化する
    - TU_QUOQUE: 君もまた。相手の過去の言動を指摘して批判をかわす
    - NO_TRUE_SCOTSMAN: 本物のスコットランド人。反証を恣意的な定義変更で回避する
"""

    def __init__(self, model):
        self.openai = OpenAI()
        self.model = model

    async def judge(self, text: str, language: str) -> FallacyAnalysisWithMetadata:
        """詭弁判定を行う"""
        try:
            response = self.openai.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                response_format=FallacyAnalysis,
            )

            message_content = response.choices[0].message.content
            response_data = json.loads(message_content)
            response_with_metadata = FallacyAnalysisWithMetadata(
                **response_data,
                llm_version=self.model,
            )
            return response_with_metadata
        except Exception as e:
            raise e
