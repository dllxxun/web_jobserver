from flask import Blueprint, request, jsonify
from src.database.models import JobPosting
from src.database.database import get_db

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    db = next(get_db())
    jobs = db.query(JobPosting).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'jobs': [{'id': job.id, 'title': job.title} for job in jobs.items],
        'total': jobs.total,
        'pages': jobs.pages
    })

@jobs_bp.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db = next(get_db())
    job = db.query(JobPosting).get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
        
    return jsonify({
        'id': job.id,
        'title': job.title,
        'company': job.company.name,
        'location': job.location
    })
