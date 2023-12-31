from datetime import datetime

from sqlalchemy.orm import Session

from domain.question.question_schema import QuestionCreate
from domain.question.question_schema import QuestionUpdate
from models import Answer
from models import Question
from models import User


def get_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ""):
    _question_list = db.query(Question)
    if keyword:
        search = "%%{}%%".format(keyword)
        sub_query = (
            db.query(Answer.question_id, Answer.content, User.username)
            .outerjoin(User, Answer.user_id == User.id)
            .subquery()
        )
        _question_list = (
            _question_list.outerjoin(User)
            .outerjoin(sub_query, sub_query.c.question_id == Question.id)
            .filter(
                Question.subject.ilike(search)  # 질문 제목
                | Question.content.ilike(search)  # 질문 내용
                | User.username.ilike(search)  # 질문 작성자
                | sub_query.c.content.ilike(search)  # 답변 내용
                | sub_query.c.username.ilike(search)  # 답변 작성자
            )
        )

    total = _question_list.distinct().count()
    question_list = (
        _question_list.order_by(Question.create_date.desc())
        .offset(skip)
        .limit(limit)
        .distinct()
        .all()
    )

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
    db_question.subject = question_update.subject  # type: ignore
    db_question.content = question_update.content  # type: ignore
    db_question.update_date = datetime.now()  # type: ignore
    db.add(db_question)
    db.commit()


def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()


# Question Model의 Voter에 현재 User를 추가
def vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.append(db_user)
    db.commit()


def cancel_vote_question(db: Session, db_question: Question, db_user: User):
    db_question.voter.remove(db_user)
    db.commit()
