from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

bookmarks_ns = Namespace('bookmarks', path='/bookmarks')

@bookmarks_ns.route('/<int:job_id>')
class Bookmark(Resource):
    @bookmarks_ns.doc('북마크 추가')
    @jwt_required()
    def post(self, job_id):
        try:
            current_user = get_jwt_identity()
            return {
                "status": "success",
                "data": {
                    "job_id": job_id,
                    "user_id": current_user
                }
            }, 201
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }, 400

@bookmarks_ns.route('/')
class BookmarkList(Resource):
    @bookmarks_ns.doc('북마크 목록 조회')
    @jwt_required()
    def get(self):
        try:
            page = request.args.get('page', 1, type=int)
            size = request.args.get('size', 10, type=int)
            
            if size > 100:
                size = 100
                
            current_user = get_jwt_identity()
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
            return {
                "status": "error",
                "message": str(e)
            }, 400