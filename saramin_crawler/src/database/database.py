from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import logging

# 데이터베이스 URL 설정
DATABASE_URL = "sqlite:///job_database.db"

# 엔진 생성 시 로깅 추가
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # SQL 쿼리 로깅
    pool_size=5,  # 커넥션 풀 크기
    max_overflow=10  # 최대 초과 커넥션
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Database session error: {e}")
        raise
    finally:
        db.close()

def check_db_connection():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        return True
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return False
    finally:
        db.close()
