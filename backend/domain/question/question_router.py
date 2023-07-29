from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question

# router 파일에는 APIRouter로 생성한 router 객체가 필요
router = APIRouter(
    prefix="/api/question",
)


# question_list 함수의 매개변수로 db: Session = Depends(get_db) 객체를 주입
@router.get("/list")
def question_list(db: Session = Depends(get_db)):
    # 질문 목록 조회
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list
