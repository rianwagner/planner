from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"msg": "Username e password são obrigatórios"}), 400

    token = AuthService.login(username, password)
    if token:
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@auth_blueprint.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({"message": "Username e password são obrigatórios"}), 400

    response, status_code = AuthService.register(username, password)
    return jsonify(response), status_code