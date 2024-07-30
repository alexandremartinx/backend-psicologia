from flask import Blueprint, jsonify, request
from services.auth_provider import authenticate
from services.jwt_handler import generate_jwt
from services.auth_guard import auth_guard
from flasgger.utils import swag_from

auth = Blueprint('auth', __name__, url_prefix='/auth')

@swag_from('swagger/auth/login.yml')
@auth.route('/login', methods=['POST'])
def auth_login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({"message": "username or password missing"}), 400

    user_data = authenticate(username, password)
    if not user_data:
        return jsonify({"message": "Invalid credentials"}), 400

    token = generate_jwt(payload=user_data, lifetime=60) # <--- generates a JWT with valid within 1 hour by now
    return jsonify({"token": token}), 200
