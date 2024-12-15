from flask import Flask, render_template
from src.crawler.job_crawler import SaraminCrawler
from src.database.database import init_db, get_db
from src.database.models import JobPosting, Company

app = Flask(__name__)
app.config.from_object('config.Config')

# before_first_request 대신 with app.app_context() 사용
with app.app_context():
    init_db()

@app.route('/')
def index():
    crawler = SaraminCrawler()
    jobs = crawler.crawl_multiple_pages(start_page=1, end_page=5)
    
    # 크롤링한 데이터를 DB에 저장
    db = next(get_db())
    for job_data in jobs:
        company = Company(
            name=job_data['company'],
            location=job_data['location']
        )
        db.add(company)
        db.commit()
        
        job = JobPosting(
            title=job_data['title'],
            company_id=company.id,
            location=job_data['location']
        )
        db.add(job)
        db.commit()
    
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
