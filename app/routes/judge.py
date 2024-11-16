from fastapi import APIRouter

from app.schemas.request import JudgeRequest
from app.schemas.response import JudgeResponse
from app.services.fallacy_analyzer import FallacyAnalyzer
from app.core.exceptions import APIException

router = APIRouter()
fallacy_analyzer = FallacyAnalyzer()


@router.post("/judge", response_model=JudgeResponse)
async def judge_fallacy(request: JudgeRequest):
    """
    入力された文字列が詭弁かどうかを判定し、分析結果を返す
    """
    # TODO エラーハンドリング
    analysis_result = await fallacy_analyzer.judge(
        text=request.text,
        language=request.language,
    )
    return JudgeResponse.from_domain(analysis_result)
