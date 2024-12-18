from flask import request
from flask_jwt_extended import create_access_token
import base64
from flask_restx import Resource, Namespace, fields
from src.utils.auth import generate_tokens, encode_password
from src.middleware.auth_middleware import auth_required
from src.database.models import User
from src.database.database import get_db

#auth_bp = Blueprint('auth', __name__)
auth_ns = Namespace('auth', description='인증 관련 API')

# 회원가입 모델
register_model = auth_ns.model('Register', {
    'email': fields.String(required=True, description='사용자 이메일', example='user@example.com'),
    'password': fields.String(required=True, description='비밀번호', example='password123'),
    'username': fields.String(required=True, description='사용자 이름', example='홍길동')
})

# 로그인 모델
login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='사용자 이메일', example='user@example.com'),
    'password': fields.String(required=True, description='비밀번호', example='password123')
})

# 응답 모델
auth_response = auth_ns.model('AuthResponse', {
    'status': fields.String(description='응답 상태'),
    'message': fields.String(description='응답 메시지'),
    'access_token': fields.String(description='액세스 토큰')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc('회원가입')
    @auth_ns.expect(register_model)
    @auth_ns.response(201, '회원가입 성공', auth_response)
    @auth_ns.response(400, '잘못된 요청')
    def post(self):
        """회원가입 API"""
        data = request.get_json()
        
        # 이메일 형식 검증
        if '@' not in data['email']:
            return {'status': 'error', 'message': '잘못된 이메일 형식입니다.'}, 400
            
        # 비밀번호 암호화
        encoded_password = base64.b64encode(data['password'].encode()).decode()
        
        # 중복 회원 검사 및 저장 로직 구현
        try:
            # DB 저장 로직 구현
            return {
                'status': 'success',
                'message': '회원가입이 완료되었습니다.'
            }, 201
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 400

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('로그인')
    @auth_ns.expect(login_model)
    @auth_ns.response(200, '로그인 성공', auth_response)
    @auth_ns.response(401, '인증 실패')
    def post(self):
        """로그인 API"""
        data = request.get_json()
        
        try:
            # 사용자 인증 로직 구현
            # DB에서 사용자 확인 후 토큰 발급
            access_token = create_access_token(identity=data['email'])
            
            return {
                'status': 'success',
                'message': '로그인 성공',
                'access_token': access_token
            }, 200
        except Exception as e:
            return {
                'status': 'error',
                'message': '로그인 실패'
            }, 401