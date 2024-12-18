from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api.models import db, Job

jobs_ns = Namespace('jobs', description='채용 공고 관련 API')

# API 모델 정의
job_model = jobs_ns.model('Job', {
    'title': fields.String(required=True, description='채용 공고 제목', example='백엔드 개발자 모집'),
    'company': fields.String(required=True, description='회사명', example='테크 컴퍼니'),
    'location': fields.String(required=True, description='근무지', example='서울시 강남구'),
    'experience': fields.String(description='요구 경력', example='3년 이상'),
    'salary': fields.String(description='급여', example='4000-5000만원'),
    'tech_stack': fields.List(fields.String, description='기술 스택', example=['Python', 'Flask', 'SQL']),
    'position': fields.String(description='채용 포지션', example='백엔드 개발자'),
    'description': fields.String(description='상세 설명')
})

@jobs_ns.route('/')
class JobList(Resource):
    @jobs_ns.doc('채용 공고 목록 조회',
        params={
            'page': {'description': '페이지 번호', 'type': 'integer', 'default': 1},
            'size': {'description': '페이지 크기', 'type': 'integer', 'default': 20},
            'location': {'description': '지역 필터', 'type': 'string'},
            'experience': {'description': '경력 필터', 'type': 'string'},
            'salary': {'description': '급여 범위 필터', 'type': 'string'},
            'tech_stack': {'description': '기술 스택 필터', 'type': 'string'},
            'keyword': {'description': '검색 키워드', 'type': 'string'},
            'company': {'description': '회사명 검색', 'type': 'string'},
            'position': {'description': '포지션 검색', 'type': 'string'},
            'sort': {'description': '정렬 기준(latest, views, salary)', 'type': 'string', 'default': 'latest'}
        })
    @jobs_ns.response(200, '성공', job_model)
    def get(self):
        """채용 공고 목록을 조회합니다."""
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)
        location = request.args.get('location')
        experience = request.args.get('experience')
        salary = request.args.get('salary')
        tech_stack = request.args.get('tech_stack')
        keyword = request.args.get('keyword')
        company = request.args.get('company')
        position = request.args.get('position')
        sort = request.args.get('sort', 'latest')

        query = Job.query

        # 필터링 적용
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        if experience:
            query = query.filter(Job.experience == experience)
        if salary:
            query = query.filter(Job.salary.ilike(f'%{salary}%'))
        if tech_stack:
            query = query.filter(Job.tech_stack.contains([tech_stack]))
        if keyword:
            query = query.filter(db.or_(
                Job.title.ilike(f'%{keyword}%'),
                Job.description.ilike(f'%{keyword}%')
            ))
        if company:
            query = query.filter(Job.company.ilike(f'%{company}%'))
        if position:
            query = query.filter(Job.position.ilike(f'%{position}%'))
        
        # 정렬 적용
        if sort == 'latest':
            query = query.order_by(Job.created_at.desc())
        elif sort == 'views':
            query = query.order_by(Job.views.desc())
        elif sort == 'salary':
            query = query.order_by(Job.salary.desc())

        # 페이지네이션 적용
        paginated_jobs = query.paginate(page=page, per_page=size)

        return {
            'jobs': [job.to_dict() for job in paginated_jobs.items],
            'total': paginated_jobs.total,
            'pages': paginated_jobs.pages,
            'current_page': page
        }
    
@jobs_ns.route('/<int:id>')
class JobDetail(Resource):
    @jobs_ns.doc('채용 공고 상세 조회',
        params={
            'id': '채용 공고 ID'
        })
    @jobs_ns.response(200, '성공', job_model)
    def get(self, id):
        """채용 공고 상세 정보를 조회합니다."""
        job = Job.query.get_or_404(id)
        
        # 조회수 증가
        job.views += 1
        db.session.commit()

        # 관련 공고 추천 (같은 기술 스택 또는 같은 포지션)
        related_jobs = Job.query.filter(
            db.or_(
                Job.tech_stack.overlap(job.tech_stack),
                Job.position == job.position
            )
        ).filter(Job.id != id).limit(5).all()

        return {
            'job': job.to_dict(),
            'related_jobs': [related.to_dict() for related in related_jobs]
        }