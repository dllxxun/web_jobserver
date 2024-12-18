from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api.models import db, Bookmark 

bookmarks_ns = Namespace('bookmarks', description='북마크 관련 API')

# API 모델 정의
bookmark_model = bookmarks_ns.model('Bookmark', {
    'job_id': fields.Integer(required=True, description='채용 공고 ID', example=1),
    'user_id': fields.Integer(description='사용자 ID'),
    'created_at': fields.DateTime(description='생성일시')
})

bookmark_list_model = bookmarks_ns.model('BookmarkList', {
    'bookmarks': fields.List(fields.Nested(bookmark_model)),
    'total': fields.Integer(description='전체 북마크 수'),
    'current_page': fields.Integer(description='현재 페이지'),
    'total_pages': fields.Integer(description='전체 페이지 수')
})

@bookmarks_ns.route('/')
class BookmarkList(Resource):
    @bookmarks_ns.doc('북마크 목록 조회',
        params={
            'page': {'description': '페이지 번호', 'type': 'integer', 'default': 1},
            'size': {'description': '페이지 크기', 'type': 'integer', 'default': 20}
        })
    @bookmarks_ns.response(200, '성공', bookmark_list_model)
    @jwt_required()
    def get(self):
        """사용자의 북마크 목록을 조회합니다."""
        current_user = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)

        bookmarks = Bookmark.query.filter_by(user_id=current_user)\
            .order_by(Bookmark.created_at.desc())\
            .paginate(page=page, per_page=size)

        return {
            'bookmarks': [bookmark.to_dict() for bookmark in bookmarks.items],
            'total': bookmarks.total,
            'current_page': page,
            'total_pages': bookmarks.pages
        }

@bookmarks_ns.route('/<int:job_id>')
class BookmarkToggle(Resource):
    @bookmarks_ns.doc('북마크 추가/제거',
        params={
            'job_id': '채용 공고 ID'
        })
    @bookmarks_ns.response(200, '성공')
    @bookmarks_ns.response(401, '인증 실패')
    @jwt_required()
    def post(self, job_id):
        """채용 공고를 북마크에 추가하거나 제거합니다."""
        current_user = get_jwt_identity()
        
        # 기존 북마크 확인
        bookmark = Bookmark.query.filter_by(
            user_id=current_user,
            job_id=job_id
        ).first()

        try:
            if bookmark:
                # 북마크 제거
                db.session.delete(bookmark)
                message = "북마크가 제거되었습니다."
            else:
                # 북마크 추가
                new_bookmark = Bookmark(user_id=current_user, job_id=job_id)
                db.session.add(new_bookmark)
                message = "북마크가 추가되었습니다."

            db.session.commit()
            return {'message': message}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 400