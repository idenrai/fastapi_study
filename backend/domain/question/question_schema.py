import datetime

from pydantic import BaseModel
from pydantic import field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

# from pydantic import ConfigDict
# from pydantic.alias_generators import to_camel


# Pydantic(https://pydantic-docs.helpmanual.io/)
# FastAPI의 입출력 스펙을 정의하고, 그 값을 검증
# - 입출력 항목의 갯수와 타입 설정
# - 입출력 항목의 필수값 체크
# - 입출력 항목의 데이터 검증
#
# 사용을 위해, 출력 스키마 작성
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    # model_config를 이용한 모델 관리
    # https://zenn.dev/tk_resilie/articles/fastapi0100_pydanticv2
    # alias_generator: JSON 시리얼라이즈를 위한 카멜 케이스 변경
    # from_attributes: sqlalchemi를 사용할 경우 필수 사용이던 orm_mode = True가 변경
    #   https://blog.turai.work/entry/20220506/1651797463
    #   다만, 현재는 이걸 사용하지 않아도 에러가 나지 않고 있다.
    # model_config = ConfigDict(
    #     alias_generator=to_camel, from_attributes=True, populate_by_name=True
    # )
    user: User | None
    # 수정이 발생할 경우에만 값이 생성되므로, Default값은 None
    update_date: datetime.datetime | None = None
    voter: list[User] = []


class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


# QuestionCreate를 상속하고, question_id만 추가
# Create에 있는 validation도 동일하게 실시
class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int


class QuestionVoteCancel(BaseModel):
    question_id: int
