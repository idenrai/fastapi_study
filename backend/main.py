from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.question import question_router

app = FastAPI()

# CORS에 예외 URL 등록
# https://developer.mozilla.org/ko/docs/Web/HTTP/CORS
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# router객체를 FastAPI App에 등록해야 라우팅 기능이 동작
app.include_router(question_router.router)