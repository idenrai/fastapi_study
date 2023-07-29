from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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


@app.get("/hello")
def hello():
    return {"message": "안녕하세요"}