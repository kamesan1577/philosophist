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
複数の詭弁が当てはまると考えた場合はすべてを出力結果に含める。
Inputにはどんな入力であろうと絶対に元の入力の忠実なコピーを入れる。
TextSpanには該当する文言の開始位置と終了位置を示す。これらの位置は決して間違えてはならず、必ず正しい位置を返すように繰り返し確認を行うこと
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
