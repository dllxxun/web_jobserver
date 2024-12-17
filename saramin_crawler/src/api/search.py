from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

search_ns = Namespace('search', path='/search')

@search_ns.route('/')
class Search(Resource):
    @search_ns.doc('고급 검색')
    @search_ns.param('query', '검색어')
    @search_ns.param('page', '페이지 번호', type=int)
    @search_ns.param('size', '페이지 크기', type=int)
    @search_ns.param('category', '카테고리')
    @search_ns.param('location', '지역')
    @search_ns.param('experience', '경력')
    @search_ns.param('job_type', '고용형태')
    @search_ns.param('salary_range', '급여범위')
    def get(self):
        try:
            query = request.args.get('query')
            page = request.args.get('page', 1, type=int)
            size = min(request.args.get('size', 10, type=int), 100)
            category = request.args.get('category')
            location = request.args.get('location')
            experience = request.args.get('experience')
            job_type = request.args.get('job_type')
            salary_range = request.args.get('salary_range')

            return {
                "status": "success",
                "data": [],
                "pagination": {
                    "currentPage": page,
                    "totalPages": 1,
                    "totalItems": 0
                },
                "filters": {
                    "category": category,
                    "location": location,
                    "experience": experience,
                    "job_type": job_type,
                    "salary_range": salary_range
                }
            }, 200
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400
