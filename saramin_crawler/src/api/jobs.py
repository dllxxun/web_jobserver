from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api.models import db, Job

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """채용 공고 목록 조회
     ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
      - name: size
        in: query
        type: integer
        required: false
        default: 20
    responses:
        200:
            description: 채용 공고 목록
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            status:
                                type: string
                            data:
                                type: array
                                items:
                                    type: object
                                    properties:
                                        id:
                                            type: integer
                                        title:
                                            type: string
    """
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)  # 페이지 크기 20으로 설정
        keyword = request.args.get('keyword')
        category = request.args.get('category')
        location = request.args.get('location')
        salary_min = request.args.get('salary_min', type=int)
        salary_max = request.args.get('salary_max', type=int)

        # 기본 쿼리 생성
        query = Job.query

        # 필터링 조건 추가
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

        # 페이지네이션 적용
        pagination = query.paginate(page=page, per_page=size)
        
        return jsonify({
            "status": "success",
            "data": [job.to_dict() for job in pagination.items],
            "pagination": {
                "currentPage": page,
                "totalPages": pagination.pages,
                "totalItems": pagination.total
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@jobs_bp.route('/jobs', methods=['POST'])
@jwt_required()
def create_job():
    """채용 공고 등록"""
    try:
        job_data = request.get_json()
        
        # 필수 필드 검증
        required_fields = ['title', 'description', 'company', 'location']
        for field in required_fields:
            if field not in job_data:
                return jsonify({
                    "status": "error",
                    "message": f"Missing required field: {field}"
                }), 400

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

        return jsonify({
            "status": "success",
            "data": new_job.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """채용 공고 상세 조회"""
    try:
        job = Job.query.get_or_404(job_id)
        return jsonify({
            "status": "success",
            "data": job.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@jobs_bp.route('/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """채용 공고 수정"""
    try:
        job = Job.query.get_or_404(job_id)
        job_data = request.get_json()

        # 필드 업데이트
        for key, value in job_data.items():
            if hasattr(job, key):
                setattr(job, key, value)

        db.session.commit()

        return jsonify({
            "status": "success",
            "data": job.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@jobs_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """채용 공고 삭제"""
    try:
        job = Job.query.get_or_404(job_id)
        db.session.delete(job)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Job deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@jobs_bp.route('/jobs/search', methods=['GET'])
def search_jobs():
    """고급 검색 기능"""
    try:
        query = request.args.get('query')
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)
        
        # 검색 쿼리 생성
        search_query = Job.query

        if query:
            search_query = search_query.filter(
                db.or_(
                    Job.title.ilike(f'%{query}%'),
                    Job.description.ilike(f'%{query}%'),
                    Job.company.ilike(f'%{query}%')
                )
            )

        # 페이지네이션 적용
        pagination = search_query.paginate(page=page, per_page=size)

        return jsonify({
            "status": "success",
            "data": [job.to_dict() for job in pagination.items],
            "pagination": {
                "currentPage": page,
                "totalPages": pagination.pages,
                "totalItems": pagination.total
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
