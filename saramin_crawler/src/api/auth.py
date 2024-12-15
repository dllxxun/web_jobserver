from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.database.models import User
from src.database.database import get_db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    db = next(get_db())
    
    if db.query(User).filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
        
    user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )
    db.add(user)
    db.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = next(get_db())
    
    user = db.query(User).filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({'token': 'your-jwt-token'})
    
    return jsonify({'error': 'Invalid credentials'}), 401
