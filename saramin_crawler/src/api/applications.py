from flask import request
from flask_restx import Resource, Namespace, fields
from src.database.models import Application
from src.database.database import get_db

applications_ns = Namespace('applications', description='지원 관리 API')

# API 모델 정의
application_model = applications_ns.model('Application', {
    'job_id': fields.Integer(required=True, description='채용 공고 ID', example=1),
    'resume': fields.String(description='이력서 첨부', example='resume.pdf')
})

application_list_model = applications_ns.model('ApplicationList', {
    'applications': fields.List(fields.Nested(application_model)),
    'total': fields.Integer(description='전체 지원 수'),
    'current_page': fields.Integer(description='현재 페이지'),
    'total_pages': fields.Integer(description='전체 페이지 수')
})

@applications_ns.route('/')
class ApplicationList(Resource):
    @applications_ns.doc('지원 내역 조회',
        params={
            'page': {'description': '페이지 번호', 'type': 'integer', 'default': 1},
            'size': {'description': '페이지 크기', 'type': 'integer', 'default': 20},
            'status': {'description': '지원 상태 필터', 'type': 'string'},
            'date_sort': {'description': '날짜 정렬 (asc/desc)', 'type': 'string', 'default': 'desc'}
        })
    @applications_ns.response(200, '성공', application_list_model)
    @jwt_required()
    def get(self):
        """사용자의 지원 내역을 조회합니다."""
        current_user = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)
        status = request.args.get('status')
        date_sort = request.args.get('date_sort', 'desc')

        return {
            'applications': [],
            'total': 0,
            'current_page': page,
            'total_pages': 0
        }

@applications_ns.route('/apply/<int:job_id>')
class ApplyJob(Resource):
    @applications_ns.doc('지원하기',
        params={
            'job_id': {'description': '채용 공고 ID', 'type': 'integer'}
        })
    @applications_ns.expect(application_model)
    @applications_ns.response(201, '지원 성공')
    @applications_ns.response(400, '잘못된 요청')
    @applications_ns.response(401, '인증 실패')
    @jwt_required()
    def post(self, job_id):
        """채용 공고에 지원합니다."""
        current_user = get_jwt_identity()
        data = request.get_json()

        try:
            return {'message': '지원이 완료되었습니다.'}, 201
        except Exception as e:
            return {'message': str(e)}, 400

@applications_ns.route('/<int:application_id>')
class CancelApplication(Resource):
    @applications_ns.doc('지원 취소',
        params={
            'application_id': {'description': '지원 ID', 'type': 'integer'}
        })
    @applications_ns.response(200, '취소 성공')
    @applications_ns.response(400, '잘못된 요청')
    @applications_ns.response(401, '인증 실패')
    @jwt_required()
    def delete(self, application_id):
        """지원 내역을 취소합니다."""
        current_user = get_jwt_identity()

        try:
            return {'message': '지원이 취소되었습니다.'}, 200
        except Exception as e:
            return {'message': str(e)}, 400