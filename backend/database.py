from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB 접속 주소
# 프로젝트의 루트 디렉토리에 저장
SQLALCHEMY_DB_URL = "sqlite:///./fastapi_study.db"

engine = create_engine(
    SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False}
)

# DB 접속을 위한 클래스
# autocommit=False의 경우에만 rollback이 동작
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()