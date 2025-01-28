from flask import request, jsonify, Blueprint
from ..services.trabalho_service import TrabalhoService
from datetime import datetime

trabalho_blueprint = Blueprint('trabalho', __name__)

@trabalho_blueprint.route('/trabalhos', methods=['GET'])
def listar_trabalhos():
    try:
        trabalhos = TrabalhoService.get_all_trabalhos()
        return jsonify([{
            "id": trabalho.id,
            "titulo": trabalho.titulo,
            "descricao": trabalho.descricao,
            "data_entrega": trabalho.data_entrega.isoformat() if trabalho.data_entrega else None,
            "materia_id": trabalho.materia_id
        } for trabalho in trabalhos]), 200
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@trabalho_blueprint.route('/trabalhos/<int:id>', methods=['GET'])
def obter_trabalho(id):
    try:
        trabalho = TrabalhoService.get_trabalho_by_id(id)
        if trabalho:
            return jsonify({
                "id": trabalho.id,
                "titulo": trabalho.titulo,
                "descricao": trabalho.descricao,
                "data_entrega": trabalho.data_entrega.isoformat() if trabalho.data_entrega else None,
                "materia_id": trabalho.materia_id
            }), 200
        else:
            return jsonify({"message": "Trabalho não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@trabalho_blueprint.route('/trabalhos', methods=['POST'])
def criar_trabalho():
    data = request.json
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    data_entrega = data.get('data_entrega')
    materia_id = data.get('materia_id')

    if not titulo or not materia_id:
        return jsonify({"message": "Campos 'titulo' e 'materia_id' são obrigatórios"}), 400

    try:
        if data_entrega:
            data_entrega = datetime.fromisoformat(data_entrega).date()
        trabalho = TrabalhoService.create_trabalho(titulo, descricao, data_entrega, materia_id)
        return jsonify({
            "id": trabalho.id,
            "titulo": trabalho.titulo,
            "descricao": trabalho.descricao,
            "data_entrega": trabalho.data_entrega.isoformat() if trabalho.data_entrega else None,
            "materia_id": trabalho.materia_id
        }), 201
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@trabalho_blueprint.route('/trabalhos/<int:id>', methods=['DELETE'])
def deletar_trabalho(id):
    try:
        success = TrabalhoService.delete_trabalho(id)
        if success:
            return jsonify({"message": "Trabalho deletado com sucesso"}), 200
        else:
            return jsonify({"message": "Trabalho não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500