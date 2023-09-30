from datetime import datetime

from sqlalchemy.orm import Session

from domain.question.question_schema import QuestionCreate
from domain.question.question_schema import QuestionUpdate
from models import Question
from models import User


def get_question_list(db: Session, skip: int = 0, limit: int = 10):
    _question_list = db.query(Question).order_by(Question.create_date.desc())
    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list


def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question


def create_question(db: Session, question_create: QuestionCreate, user: User):
    db_question = Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_question)
    db.commit()


def update_question(
    db: Session, db_question: Question, question_update: QuestionUpdate
):
    db_question = Question(
        subject=question_update.subject,
        content=question_update.content,
        modify_date=datetime.now(),
    )
    db.add(db_question)
    db.commit()
