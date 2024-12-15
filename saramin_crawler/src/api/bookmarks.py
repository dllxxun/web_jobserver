from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database.database import get_db
from src.database.models import Bookmark, JobPosting
from sqlalchemy import desc

bookmarks_bp = Blueprint('bookmarks', __name__)

@bookmarks_bp.route('/bookmarks', methods=['POST'])
@jwt_required()
def toggle_bookmark():
    user_id = get_jwt_identity()
    job_id = request.json.get('job_id')
    
    db = next(get_db())
    bookmark = db.query(Bookmark).filter_by(user_id=user_id, job_id=job_id).first()
    
    if bookmark:
        db.delete(bookmark)
        message = "Bookmark removed"
    else:
        new_bookmark = Bookmark(user_id=user_id, job_id=job_id)
        db.add(new_bookmark)
        message = "Bookmark added"
    
    db.commit()
    return jsonify({"message": message}), 200

@bookmarks_bp.route('/bookmarks', methods=['GET'])
@jwt_required()
def get_bookmarks():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')
    
    db = next(get_db())
    query = db.query(JobPosting).join(Bookmark).filter(Bookmark.user_id == user_id)
    
    # 필터링
    location = request.args.get('location')
    if location:
        query = query.filter(JobPosting.location.ilike(f'%{location}%'))
    
    experience = request.args.get('experience')
    if experience:
        query = query.filter(JobPosting.experience == experience)
    
    salary = request.args.get('salary')
    if salary:
        query = query.filter(JobPosting.salary >= salary)
    
    tech_stack = request.args.get('tech_stack')
    if tech_stack:
        query = query.filter(JobPosting.tech_stack.ilike(f'%{tech_stack}%'))
    
    # 검색
    keyword = request.args.get('keyword')
    if keyword:
        query = query.filter(JobPosting.title.ilike(f'%{keyword}%') |
                             JobPosting.company.has(name=keyword) |
                             JobPosting.description.ilike(f'%{keyword}%'))
    
    # 정렬
    if sort_order == 'desc':
        query = query.order_by(desc(getattr(JobPosting, sort_by)))
    else:
        query = query.order_by(getattr(JobPosting, sort_by))
    
    bookmarks = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        "bookmarks": [{"id": b.id, "title": b.title, "company": b.company.name} for b in bookmarks.items],
        "total": bookmarks.total,
        "pages": bookmarks.pages,
        "current_page": bookmarks.page
    }), 200

@bookmarks_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job_detail(job_id):
    db = next(get_db())
    job = db.query(JobPosting).get(job_id)
    
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    # 조회수 증가
    job.views += 1
    db.commit()
    
    # 관련 공고 추천 (같은 회사의 다른 공고)
    related_jobs = db.query(JobPosting).filter(JobPosting.company_id == job.company_id, 
                                               JobPosting.id != job.id).limit(5).all()
    
    return jsonify({
        "id": job.id,
        "title": job.title,
        "company": job.company.name,
        "location": job.location,
        "description": job.description,
        "salary": job.salary,
        "experience": job.experience,
        "views": job.views,
        "related_jobs": [{"id": rj.id, "title": rj.title} for rj in related_jobs]
    }), 200
