from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import create_access_token

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"msg": "Username e password são obrigatórios"}), 400

    user = AuthService.login(username, password)
    if user:
        access_token = create_access_token(identity=user.id)  # Agora vai funcionar!
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"message": "Username e password são obrigatórios"}), 400

    response, status_code = AuthService.register(username, password)
    return jsonify(response), status_code