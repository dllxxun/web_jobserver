from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import timedelta
from src.crawler.job_crawler import SaraminCrawler
from src.database.database import init_db, get_db
from src.database.models import JobPosting, Company
from src.api.auth import auth_bp
from src.api.jobs import jobs_bp
from src.api.applications import applications_bp
from src.api.bookmarks import bookmarks_bp
from src.api.notification import notifications_bp
from src.api.search import search_bp
from src.api.statistics import statistics_bp
from src.api.models import db



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# JWT 설정
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Swagger 설정
SWAGGER_URL = '/api/docs'
API_URL = 'http://113.198.66.75:19186/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "OurJobs API Documentation"
    }
)

# Blueprint 등록
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(jobs_bp, url_prefix='/api')
app.register_blueprint(applications_bp, url_prefix='/api')
app.register_blueprint(bookmarks_bp, url_prefix='/api')
app.register_blueprint(search_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(notifications_bp)

# Database initialization
with app.app_context():
    init_db()

@app.route('/')
def index():
    try:
        crawler = SaraminCrawler()
        jobs = crawler.crawl_multiple_pages(start_page=1, end_page=5)
        
        # 크롤링한 데이터를 DB에 저장
        db = next(get_db())
        try:
            for job_data in jobs:
                # 기존 회사 검색
                existing_company = db.query(Company).filter_by(
                    name=job_data['company']
                ).first()
                
                if not existing_company:
                    company = Company(
                        name=job_data['company'],
                        location=job_data['location']
                    )
                    db.add(company)
                    db.commit()
                else:
                    company = existing_company
                
                # 중복 채용공고 확인
                existing_job = db.query(JobPosting).filter_by(
                    title=job_data['title'],
                    company_id=company.id
                ).first()
                
                if not existing_job:
                    job = JobPosting(
                        title=job_data['title'],
                        company_id=company.id,
                        location=job_data['location']
                    )
                    db.add(job)
                    db.commit()
            
            return render_template('index.html', jobs=jobs)
            
        except Exception as e:
            db.rollback()
            return f"Database error: {str(e)}"
        finally:
            db.close()
            
    except Exception as e:
        return f"Crawling error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19186)
