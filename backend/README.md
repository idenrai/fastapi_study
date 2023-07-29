# fastapi_study backend
## 환경설정
[pyenv 설치](https://idenrai.tistory.com/273)

파이썬 설치 및 가상환경 만들기

```commandline
pyenv install 3.11.4
python global 3.11.4
pyenv virtualenv 3.11.4 venv
pyenv activate venv
pip install --upgrade pip
```

Package Install

```commandline
pip install -r requirements.txt
```

## 실행
uvicorn 실행

```commandline
uvicorn main:app --reroad
```

## 폴더 구조

```text
backend
├── main.py     : FastAPI의 전체적인 환경 설정
├── database.py : DB 관련 설정
├── models.py   : 모델 클래스 정의
└── domain      : API
    ├── answer
    ├── question
    └── user
```

## 그 외
[Documents](http://127.0.0.1:8000/docs)

