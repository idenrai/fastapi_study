from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_crud
from domain.question import question_schema

"""
MEMO
FastAPI의 API 함수는 비동기 함수로도 사용할 수 있다.
https://fastapi.tiangolo.com/async/
"""
# router 파일에는 APIRouter로 생성한 router 객체가 필요
router = APIRouter(
    prefix="/api/question",
)


# @router.get Annotation에 response_model을 추가
# => question_list의 리턴값이 Question 스키마로 구성된 리스트임을 의미
# question_list 함수의 매개변수로 db: Session = Depends(get_db) 객체를 주입
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    # 질문 목록 조회
    _question_list = question_crud.get_question_list(db)
    return _question_list


@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    # 질문 목록 조회
    question = question_crud.get_question(db, question_id=question_id)
    return question


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(
    _question_create: question_schema.QuestionCreate,
    db: Session = Depends(get_db),
):
    question_crud.create_question(db, question_create=_question_create)
