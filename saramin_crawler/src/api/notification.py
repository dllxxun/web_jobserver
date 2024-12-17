from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

notifications_ns = Namespace('notifications', path='/notifications')

@notifications_ns.route('/settings')
class NotificationSettings(Resource):
    @notifications_ns.doc('알림 설정 업데이트')
    @jwt_required()
    def post(self):
        try:
            current_user = get_jwt_identity()
            settings_data = request.get_json()
            return {
                "status": "success",
                "data": {
                    "email_notifications": settings_data.get('email_notifications', False),
                    "push_notifications": settings_data.get('push_notifications', False),
                    "notification_types": settings_data.get('notification_types', [])
                }
            }, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

@notifications_ns.route('/')
class NotificationList(Resource):
    @notifications_ns.doc('알림 목록 조회')
    @notifications_ns.param('page', '페이지 번호', type=int)
    @notifications_ns.param('size', '페이지 크기', type=int)
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            page = request.args.get('page', 1, type=int)
            size = min(request.args.get('size', 10, type=int), 100)
            return {
                "status": "success",
                "data": [],
                "pagination": {
                    "currentPage": page,
                    "totalPages": 1,
                    "totalItems": 0
                }
            }, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
