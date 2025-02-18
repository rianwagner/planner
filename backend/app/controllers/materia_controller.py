from flask import request, jsonify, Blueprint
from ..services.materia_service import MateriaService
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

materia_blueprint = Blueprint('materia', __name__)

@materia_blueprint.route('/materias', methods=['GET'])
@jwt_required()
def listar_materias():
    try:
        user_id = get_jwt_identity()
        materias = MateriaService.get_materias_by_user(user_id)
        return jsonify([{"id": materia.id, "nome": materia.nome} for materia in materias]), 200
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@materia_blueprint.route('/materias/<int:id>', methods=['GET'])
def obter_materia(id):
    try:
        materia = MateriaService.get_materia_by_id(id)
        if materia:
            return jsonify({"id": materia.id, "nome": materia.nome}), 200
        else:
            return jsonify({"message": "Matéria não encontrada"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@materia_blueprint.route('/materias', methods=['POST'])
@jwt_required()
def criar_materia():
    nome = request.json.get('nome')
    if not nome:
        return jsonify({"message": "O campo 'nome' é obrigatório"}), 400

    try:
        materia = MateriaService.create_materia(nome)
        return jsonify({"id": materia.id, "nome": materia.nome}), 201
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@materia_blueprint.route('/materias/<int:id>', methods=['DELETE'])
@jwt_required()
def deletar_materia(id):
    try:
        success = MateriaService.delete_materia(id)
        if success:
            return jsonify({"message": "Matéria deletada com sucesso"}), 200
        else:
            return jsonify({"message": "Matéria não encontrada"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500
    
@materia_blueprint.route('/materias/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_materia(id):
    try:
        data = request.get_json()
        nome = data.get('nome')

        if not nome:
            return jsonify({"message": "O campo 'nome' é obrigatório"}), 400

        materia = MateriaService.get_by_id(id)
        if not materia:
            return jsonify({"message": "Matéria não encontrada"}), 404

        materia_atualizada = MateriaService.update_materia(materia, nome)
        if materia_atualizada:
            return jsonify({"message": "Matéria atualizada com sucesso"}), 200
        else:
            return jsonify({"message": "Erro ao atualizar a matéria"}), 500
    except Exception as e:
        print(f"Erro ao atualizar matéria: {e}")
        return jsonify({"message": "Erro interno no servidor"}), 500