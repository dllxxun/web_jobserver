from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from datetime import timedelta
import base64

def generate_tokens(user_id):
    access_token = create_access_token(
        identity=user_id,
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        identity=user_id,
        expires_delta=timedelta(days=30)
    )
    return access_token, refresh_token

def encode_password(password):
    return base64.b64encode(password.encode()).decode()

def decode_password(encoded_password):
    return base64.b64decode(encoded_password.encode()).decode()
