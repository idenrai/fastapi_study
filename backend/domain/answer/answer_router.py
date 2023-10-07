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
    prefix="/answers",
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


# 답변 조회
@router.get("/detail/{answer_id}", response_model=answer_schema.Answer)
def answer_detail(answer_id: int, db: Session = Depends(get_db)):
    answer = answer_crud.get_answer(db, answer_id=answer_id)
    return answer


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def answer_update(
    _answer_update: answer_schema.AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_update.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="데이터를 찾을 수 없습니다."
        )

    if current_user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="삭제 권한이 없습니다."
        )

    answer_crud.update_answer(db=db, db_answer=db_answer, answer_update=_answer_update)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(
    _answer_delete: answer_schema.AnswerDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_delete.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="데이터를 찾을 수 없습니다."
        )

    if current_user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="삭제 권한이 없습니다."
        )

    answer_crud.delete_answer(db=db, db_answer=db_answer)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote(
    _answer_vote: answer_schema.AnswerVote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="데이터를 찾을 수 없습니다."
        )

    answer_crud.vote_answer(db, db_answer=db_answer, db_user=current_user)


@router.delete("/vote", status_code=status.HTTP_204_NO_CONTENT)
def answer_vote_cancel(
    _answer_vote_cancel: answer_schema.AnswerVoteCancel,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote_cancel.answer_id)

    if not db_answer or current_user not in db_answer.voter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="데이터를 찾을 수 없습니다."
        )

    answer_crud.cancel_vote_answer(db=db, db_answer=db_answer, db_user=current_user)
