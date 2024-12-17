from flask import request
from flask_restx import Resource, Namespace
from src.utils.auth import generate_tokens, encode_password
from src.middleware.auth_middleware import auth_required
from src.database.models import User
from src.database.database import get_db

#auth_bp = Blueprint('auth', __name__)
auth_ns = Namespace('auth', path='/auth')

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.doc('회원가입')
    def post(self):
        data = request.get_json()
        db = next(get_db())
        
        encoded_password = encode_password(data['password'])
        user = User(
            username=data['username'],
            email=data['email'],
            password=encoded_password
        )
        db.add(user)
        db.commit()
        
        return {'message': 'User registered successfully'}, 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('로그인')
    def post(self):
        data = request.get_json()
        db = next(get_db())
        
        user = db.query(User).filter_by(email=data['email']).first()
        if user and encode_password(data['password']) == user.password:
            access_token, refresh_token = generate_tokens(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        
        return {'error': 'Invalid credentials'}, 401
