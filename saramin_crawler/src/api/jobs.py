from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api.models import db, Job

jobs_ns = Namespace('jobs', path='/jobs')

# API 모델 정의
job_model = jobs_ns.model('Job', {
    'title': fields.String(required=True, description='채용 공고 제목'),
    'description': fields.String(required=True, description='상세 설명'),
    'company': fields.String(required=True, description='회사명'),
    'location': fields.String(required=True, description='근무지'),
    'salary_range': fields.String(description='급여 범위'),
    'requirements': fields.List(fields.String, description='요구사항'),
    'category': fields.String(description='카테고리'),
    'job_type': fields.String(description='고용 형태')
})

@jobs_ns.route('/')
class JobList(Resource):
    @jobs_ns.doc('채용 공고 목록 조회',
        params={
            'page': {'description': '페이지 번호', 'type': 'integer', 'default': 1},
            'size': {'description': '페이지 크기', 'type': 'integer', 'default': 10},
            'keyword': {'description': '검색어', 'type': 'string'},
            'category': {'description': '카테고리', 'type': 'string'},
            'location': {'description': '지역', 'type': 'string'},
            'salary_min': {'description': '최소 급여', 'type': 'int'},
            'salary_max': {'description': '최대 급여', 'type': 'int'}
        })
    def get(self):
        """채용 공고 목록을 조회합니다."""
        pass
    def get(self):
        try:
            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 20))
            keyword = request.args.get('keyword')
            category = request.args.get('category')
            location = request.args.get('location')
            salary_min = request.args.get('salary_min', type=int)
            salary_max = request.args.get('salary_max', type=int)

            query = Job.query

            if keyword:
                query = query.filter(Job.title.ilike(f'%{keyword}%'))
            if category:
                query = query.filter(Job.category == category)
            if location:
                query = query.filter(Job.location.ilike(f'%{location}%'))
            if salary_min:
                query = query.filter(Job.salary_range >= salary_min)
            if salary_max:
                query = query.filter(Job.salary_range <= salary_max)

            pagination = query.paginate(page=page, per_page=size)
            
            return {
                "status": "success",
                "data": [job.to_dict() for job in pagination.items],
                "pagination": {
                    "currentPage": page,
                    "totalPages": pagination.pages,
                    "totalItems": pagination.total
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @jobs_ns.doc('채용 공고 등록')
    @jobs_ns.expect(job_model)
    @jobs_ns.response(201, '생성 성공')
    def post(self):
        """새로운 채용 공고를 등록합니다."""
        pass
    @jwt_required()
    def post(self):
        try:
            job_data = request.get_json()
            new_job = Job(
                title=job_data['title'],
                description=job_data['description'],
                company=job_data['company'],
                location=job_data['location'],
                salary_range=job_data.get('salary_range'),
                requirements=job_data.get('requirements', []),
                category=job_data.get('category', '기타'),
                job_type=job_data.get('job_type', '정규직')
            )
            db.session.add(new_job)
            db.session.commit()
            return {"status": "success", "data": new_job.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 400

@jobs_ns.route('/<int:job_id>')
class Job(Resource):
    @jobs_ns.doc('채용 공고 상세 조회')
    def get(self, job_id):
        try:
            job = Job.query.get_or_404(job_id)
            return {"status": "success", "data": job.to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

    @jobs_ns.doc('채용 공고 수정')
    @jobs_ns.expect(job_model)
    @jwt_required()
    def put(self, job_id):
        try:
            job = Job.query.get_or_404(job_id)
            job_data = request.get_json()
            for key, value in job_data.items():
                if hasattr(job, key):
                    setattr(job, key, value)
            db.session.commit()
            return {"status": "success", "data": job.to_dict()}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 400

    @jobs_ns.doc('채용 공고 삭제')
    @jwt_required()
    def delete(self, job_id):
        try:
            job = Job.query.get_or_404(job_id)
            db.session.delete(job)
            db.session.commit()
            return {"status": "success", "message": "Job deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}, 400

@jobs_ns.route('/search')
class JobSearch(Resource):
    @jobs_ns.doc('채용 공고 검색')
    @jobs_ns.param('query', '검색어')
    @jobs_ns.param('page', '페이지 번호', type=int, default=1)
    @jobs_ns.param('size', '페이지 크기', type=int, default=20)
    def get(self):
        try:
            query = request.args.get('query')
            page = int(request.args.get('page', 1))
            size = int(request.args.get('size', 20))
            
            search_query = Job.query
            if query:
                search_query = search_query.filter(
                    db.or_(
                        Job.title.ilike(f'%{query}%'),
                        Job.description.ilike(f'%{query}%'),
                        Job.company.ilike(f'%{query}%')
                    )
                )

            pagination = search_query.paginate(page=page, per_page=size)
            return {
                "status": "success",
                "data": [job.to_dict() for job in pagination.items],
                "pagination": {
                    "currentPage": page,
                    "totalPages": pagination.pages,
                    "totalItems": pagination.total
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400