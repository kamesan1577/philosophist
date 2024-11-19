from pyexpat import model
from fastapi import APIRouter, Security

from app.schemas.request import JudgeRequest
from app.schemas.response import JudgeResponse
from app.services.fallacy_analyzer import FallacyAnalyzer
from app.core.exceptions import APIException
from app.core.auth import basic_auth

router = APIRouter()
fallacy_analyzer = FallacyAnalyzer()


@router.post(
    "/judge", response_model=JudgeResponse, dependencies=[Security(basic_auth)]
)
async def judge_fallacy(request: JudgeRequest):
    """
    入力された文字列が詭弁かどうかを判定し、分析結果を返す。
    複数の詭弁が当てはまると考えた場合はすべてを出力結果に含める。
    TextSpanには該当する文言の開始位置と終了位置を示す。これらの位置は決して間違えてはならず、必ず正しい位置を返すように繰り返し確認を行うこと
    """
    # TODO エラーハンドリング
    analysis_result = await fallacy_analyzer.judge(
        text=request.text,
        language=request.language,
    )
    return JudgeResponse.from_domain(analysis_result)
