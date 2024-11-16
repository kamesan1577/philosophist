from pydantic import BaseModel, Field


class JudgeRequest(BaseModel):
    text: str = Field(..., description="詭弁かどうかを判定する文字列")
    language: str = Field(default="ja", description="テキストの言語")
