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
    詭弁かどうかを判定してください。
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
