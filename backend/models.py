from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from database import Base

# SQLAlchemy
# https://docs.sqlalchemy.org/en/13/core/type_basics.html

# 테이블 객체
# 다대다의 관계 적용을 위한 테이블 작성
question_voter = Table(
    "question_voter",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("question.id"), primary_key=True),
)

answer_voter = Table(
    "answer_voter",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("answer_id", Integer, ForeignKey("answer.id"), primary_key=True),
)


# 질문 모델
class Question(Base):
    __tablename__ = "question"

    # PK + Integer는 값을 자동으로 증가시킨다
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="question_users")
    # Model을 통해 Voter 저장시, 실제 데이터는 secondary에 지정한 테이블에 저장되며, voter를 통해 참조
    voter = relationship("User", secondary=question_voter, backref="question_voters")


# 답변 모델
# relationship을 사용하여, question의 다른 answers를 역참조 가능하게 함
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    update_date = Column(DateTime, nullable=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref="answers")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    voter = relationship("User", secondary=answer_voter, backref="answer_voters")


# 유저 모델
#
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
