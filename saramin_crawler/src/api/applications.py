from flask import Blueprint, request, jsonify
from src.database.models import Application
from src.database.database import get_db

applications_bp = Blueprint('applications', __name__)

@applications_bp.route('/apply/<int:job_id>', methods=['POST'])
def apply_job(job_id):
    db = next(get_db())
    application = Application(
        user_id=request.user_id,  # JWT에서 추출
        job_id=job_id
    )
    db.add(application)
    db.commit()
    
    return jsonify({'message': 'Application submitted successfully'})

@applications_bp.route('/applications', methods=['GET'])
def get_applications():
    db = next(get_db())
    applications = db.query(Application).filter_by(user_id=request.user_id).all()
    
    return jsonify({
        'applications': [{
            'job_id': app.job_id,
            'status': app.status
        } for app in applications]
    })
