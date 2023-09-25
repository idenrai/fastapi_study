from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB 접속 주소
# 프로젝트의 루트 디렉토리에 저장
SQLALCHEMY_DB_URL = "sqlite:///./fastapi_study.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

# DB 접속을 위한 클래스
# autocommit=False의 경우에만 rollback이 동작
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLite의 설정 수정
# PK, UK 등의 제약 조건의 이름을 따로 정의하지 않을 경우, 제약 조건에 이름이 없다는 오류가 발생
# 이를 막기 위해, 아래를 수동으로 설정
Base = declarative_base()
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base.metadata = MetaData(naming_convention=naming_convention)


# FastAPI DI
# DB 세션 객체를 리턴하는 제네레이터를 생성
# 제네레이터 : https://wikidocs.net/134909
def get_db():
    # 세션 생성
    db = SessionLocal()
    try:
        yield db
    finally:
        # Session을 커넥션 풀에 반환 (종료 아님)
        # 세션 객체 생성 후 db.close()를 실행하지 않으면, 커넥션 풀에 db세션이 반환되지 않아 문제가 생김
        db.close()
