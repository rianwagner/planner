from flask import request, jsonify, Blueprint
from ..services.materia_service import MateriaService

materia_blueprint = Blueprint('materia', __name__)

@materia_blueprint.route('/materias', methods=['GET'])
def listar_materias():
    try:
        materias = MateriaService.get_all_materias()
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
def deletar_materia(id):
    try:
        success = MateriaService.delete_materia(id)
        if success:
            return jsonify({"message": "Matéria deletada com sucesso"}), 200
        else:
            return jsonify({"message": "Matéria não encontrada"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500