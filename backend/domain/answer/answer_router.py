from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from database import get_db
from domain.answer import answer_crud
from domain.answer import answer_schema
from domain.question import question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/answer",
)


# 답글을 작성하는 라우터이므로, 출력은 없음
# 출력이 없으므로, 204를 리턴하여 응답이 없음을 표현
@router.post("/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def answer_create(
    question_id: int,
    _answer_create: answer_schema.AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 질문 검색
    question = question_crud.get_question(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # 질문이 존재할 경우 답변 생성
    answer_crud.create_answer(
        db, question=question, answer_create=_answer_create, user=current_user
    )

    # Redirect
    from domain.question.question_router import router as question_router

    url = question_router.url_path_for("question_detail", question_id=question_id)
    return RedirectResponse(url, status_code=303)
