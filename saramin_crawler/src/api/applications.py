from flask import request
from flask_restx import Resource, Namespace
from src.database.models import Application
from src.database.database import get_db

applications_ns = Namespace('applications', path='/applications')


@applications_ns.route('/apply/<int:job_id>')
class ApplyJob(Resource):
    @applications_ns.doc('지원하기')
    def post(self, job_id):
        db = next(get_db())
        application = Application(
            user_id=request.user_id,
            job_id=job_id
        )
        db.add(application)
        db.commit()
        
        return {'message': 'Application submitted successfully'}

@applications_ns.route('/')
class Applications(Resource):
    @applications_ns.doc('지원 내역 조회')
    def get(self):
        db = next(get_db())
        applications = db.query(Application).filter_by(user_id=request.user_id).all()
        
        return {
            'applications': [{
                'job_id': app.job_id,
                'status': app.status
            } for app in applications]
        }