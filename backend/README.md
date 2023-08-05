# fastapi_study backend

## 환경설정

[pyenv 설치](https://idenrai.tistory.com/273)

### 파이썬 설치 및 가상환경 만들기

```commandline
pyenv install 3.11.4
python global 3.11.4
pyenv virtualenv 3.11.4 venv
pyenv activate venv
pip install --upgrade pip
```

### Package Install

```commandline
pip install -r requirements.txt
```

### SQLite Install

```commandline
brew install --cask db-browser-for-sqlite
```

### File Watcher Plugin

- Settings → Plugins → `file watchers` 검색 및 설치
- Settings → Tools → File Watchers에서 `watchers.xml`을 import
- 자세한 설정은 아래 참조
  - <https://nnamm.work/blog/004-write-cleancode-with-pycharm/>

## 실행

```commandline
pyenv activate venv
```

uvicorn 실행

```commandline
uvicorn main:app --reload
```

## DB 관리

SQLAlchemy로 작성한 모델을 기반으로 데이터베이스를 관리
models.py 파일에 작성한 모델을 이용하여 테이블을 생성, 변경 가능

### 테이블 내용 변경시

models의 내용 변경시 리비전을 통해 테이블 생성&변경

```commandline
alembic revision --autogenerate
```

리비전 파일을 실행하여, `fastapi_study.db` 파일을 생성

```commandline
alembic upgrade head
```

생성된 `fastapi_study.db` 파일은 DB Browser for SQLite에서 확인 가능

### (초기 구축시에만 실시)

초기화를 통해 alembic.ini 생성

```commandline
alembic init migrations
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
