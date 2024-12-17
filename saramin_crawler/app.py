from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource, fields
from datetime import timedelta
from src.crawler.job_crawler import SaraminCrawler
from src.database.database import init_db, get_db
from src.database.models import JobPosting, Company
from src.api.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# JWT 설정
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

# Swagger UI 설정
api = Api(
    app,
    version='1.0',
    title='Ours Job Management',
    description='swagger..',
    doc='/swagger/',
    prefix='/api',
    default='default',  # 기본 네임스페이스 설정
    default_label='Default Namespace',  # 기본 네임스페이스 라벨
    contact='cyj0749@naver.com',
    contact_email='cyj0749@naver.com',
    ui=True,  # Swagger UI 활성화
    validate=True  # 요청 유효성 검사 활성화
)


# Database initialization
with app.app_context():
    init_db()

@app.route('/')
def index():
    try:
        crawler = SaraminCrawler()
        jobs = crawler.crawl_multiple_pages(start_page=1, end_page=5)
        
        db = next(get_db())
        try:
            for job_data in jobs:
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

# API 모델 정의
job_model = api.model('Job', {
    'title': fields.String(required=True, description='채용 공고 제목'),
    'company': fields.String(required=True, description='회사명'),
    'location': fields.String(required=True, description='근무지'),
    'description': fields.String(description='상세 설명')
})

# Namespace 등록
from src.api.auth import auth_ns
from src.api.jobs import jobs_ns
from src.api.applications import applications_ns
from src.api.bookmarks import bookmarks_ns
from src.api.search import search_ns
from src.api.statistics import statistics_ns
from src.api.notification import notifications_ns

# API 그룹화
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(jobs_ns, path='/jobs')
api.add_namespace(applications_ns, path='/applications')
api.add_namespace(bookmarks_ns, path='/bookmarks')
api.add_namespace(search_ns, path='/search')
api.add_namespace(statistics_ns, path='/statistics')
api.add_namespace(notifications_ns, path='/notifications')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=19186, debug=True)
