# web_jobserver

# OurJobs - 채용정보 크롤링 웹사이트

## 프로젝트 소개
사람인 웹사이트의 채용정보를 크롤링하여 제공하는 웹 서비스입니다.

## 기술 스택
- Python 3.9
- Flask
- SQLAlchemy
- BeautifulSoup4
- HTML/CSS
- SQLite

## 설치 및 실행 방법

1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate 
2. 필요한 패키지 설치
pip install -r requirements.txt
3. 데이터베이스 초기화
flask db init
flask db migrate
flask db upgrade
4. 애플리케이션 실행
flask run --host=0.0.0.0 --port=19186

## API 문서
- Swagger UI: http://113.198.66.75:19186/api/docs