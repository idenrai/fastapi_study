from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_crud
from domain.question import question_schema
from domain.user.user_router import get_current_user
from models import User

"""
MEMO
FastAPI의 API 함수는 비동기 함수로도 사용할 수 있다.
https://fastapi.tiangolo.com/async/
"""
# router 파일에는 APIRouter로 생성한 router 객체가 필요
router = APIRouter(
    prefix="/questions",
)


# @router.get Annotation에 response_model을 추가
# => question_list의 리턴값이 Question 스키마로 구성된 리스트임을 의미
# question_list 함수의 매개변수로 db: Session = Depends(get_db) 객체를 주입
@router.get("/", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    # 질문 목록 조회
    total, _question_list = question_crud.get_question_list(
        db, skip=page * size, limit=size
    )
    return {"total": total, "question_list": _question_list}


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    # 질문 목록 조회
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    _question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question_crud.create_question(
        db, question_create=_question_create, user=current_user
    )


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
def question_update(
    _question_update: question_schema.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_question = question_crud.get_question(
        db, question_id=_question_update.question_id
    )
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="데이터를 찾을 수 없습니다."
        )
    if current_user.id != db_question.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="수정 권한이 없습니다."
        )

    question_crud.update_question(
        db=db, db_question=db_question, question_update=_question_update
    )


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(
    _question_delete: question_schema.QuestionDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_question = question_crud.get_question(
        db, question_id=_question_delete.question_id
    )
    if not db_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="데이터를 찾을 수 없습니다."
        )
    if current_user.id != db_question.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="삭제 권한이 없습니다."
        )

    question_crud.delete_question(db=db, db_question=db_question)
