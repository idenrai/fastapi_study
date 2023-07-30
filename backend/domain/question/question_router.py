from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

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
