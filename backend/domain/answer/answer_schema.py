import datetime

from pydantic import BaseModel
from pydantic import field_validator

from domain.user.user_schema import User


# 입력 항목을 처리할 스키마
# get이 아닌 다른 방식의 입력값은 Pydantic 스키마로만 읽을 수 있다
# 반대로 get은 각각의 입력 항목을 라우터 함수의 매개변수로 읽어야 한다
class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    # 수정이 발생할 경우에만 값이 생성되므로, Default값은 None
    update_date: datetime.datetime | None = None

    class Config:
        orm_mode = True


class AnswerCreate(BaseModel):
    content: str

    @field_validator("content")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int
