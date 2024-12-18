import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('job_database.db')
cursor = conn.cursor()

# 크롤링 데이터를 위한 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS crawled_jobs (
    job_id INTEGER PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary TEXT,
    experience TEXT,
    tech_stack TEXT,
    description TEXT,
    created_at TEXT,
    views INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active'
)
''')

# 샘플 데이터 삽입
crawled_data = [
    (1, "백엔드 개발자", "테크 컴퍼니", "서울 강남구", "4000-5000만원", "3년 이상", 
     "Python, Flask, MySQL", "백엔드 개발자 채용", "2024-12-18", 0, "active"),
    (2, "프론트엔드 개발자", "웹 솔루션즈", "서울 서초구", "3500-4500만원", "신입", 
     "JavaScript, React, HTML/CSS", "프론트엔드 개발자 채용", "2024-12-18", 0, "active"),
    (3, "데이터 엔지니어", "데이터 컴퍼니", "서울 송파구", "4500-5500만원", "5년 이상",
     "Python, SQL, Hadoop, Spark", "데이터 엔지니어링 포지션", "2024-12-18", 0, "active")
]

cursor.executemany('''
INSERT INTO crawled_jobs (job_id, title, company, location, salary, experience, 
                         tech_stack, description, created_at, views, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', crawled_data)

# 변경사항 저장
conn.commit()

# SQL 덤프 파일로 내보내기
with open('crawled-data.sql', 'w', encoding='utf-8') as f:
    for line in conn.iterdump():
        f.write('%s\n' % line)

# 연결 종료
conn.close()
