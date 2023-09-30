from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator


# Pydantic(https://pydantic-docs.helpmanual.io/)
# FastAPI의 입출력 스펙을 정의하고, 그 값을 검증
# - 입출력 항목의 갯수와 타입 설정
# - 입출력 항목의 필수값 체크
# - 입출력 항목의 데이터 검증
#
# 사용을 위해, 출력 스키마 작성
class UserCreate(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    @field_validator("username", "password1", "password2", "email")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    # field_validator와 validator의 차이 예시
    # https://zenn.dev/tkrk/articles/4045f3b4f9189f#%40validator%E3%81%AE%E5%BB%83%E6%AD%A2
    # values["aaa"] 에서 values.data["aaa"] 로 바뀜
    @field_validator("password2", "password1")
    def password_match(cls, v, values):
        if "password1" in values.data and v != values.data["password1"]:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v


# User Login 시에 발행할 토큰
# FastAPI의 security패키지를 통해 OAuth2 인증을 실시
# 로그인 시 받아온 토큰은 질답 작성 등 유저 정보가 필요한 API를 호출할 때 필요
# 액세스 토큰을 FE에 저장해 두고, API 호출시마다 HTTP 헤더에 토큰을 담아 요청
class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True
