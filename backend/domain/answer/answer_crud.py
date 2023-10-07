from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer.answer_schema import AnswerCreate
from domain.answer.answer_schema import AnswerUpdate
from models import Answer
from models import Question
from models import User


def create_answer(
    db: Session, question: Question, answer_create: AnswerCreate, user: User
):
    db_answer = Answer(
        question=question,
        content=answer_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_answer)
    db.commit()


def get_answer(db: Session, answer_id: int):
    return db.query(Answer).get(answer_id)


def update_answer(db: Session, db_answer: Answer, answer_update: AnswerUpdate):
    db_answer.content = answer_update.content  # type: ignore
    db_answer.update_date = datetime.now()  # type: ignore
    db.add(db_answer)  # type: ignore
    db.commit()


def delete_answer(db: Session, db_answer: Answer):
    db.delete(db_answer)
    db.commit()


# Question Model의 Voter에 현재 User를 추가
def vote_answer(db: Session, db_answer: Answer, db_user: User):
    db_answer.voter.append(db_user)
    db.commit()


def cancel_vote_answer(db: Session, db_answer: Answer, db_user: User):
    db_answer.voter.remove(db_user)
    db.commit()
