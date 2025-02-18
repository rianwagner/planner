from flask import request, jsonify, Blueprint
from ..services.prova_service import ProvaService
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from datetime import datetime

prova_blueprint = Blueprint('prova', __name__)

@prova_blueprint.route('/provas', methods=['GET'])
@jwt_required()
def listar_provas():
    try:
        user_id = get_jwt_identity()
        provas = ProvaService.get_provas_by_user(user_id)
        return jsonify([{"id": prova.id, 
                         "titulo": prova.titulo, 
                         "materia_id": prova.materia_id, 
                         "descricao": prova.descricao, 
                         "data": prova.data_prova.strftime("%Y-%m-%d") if prova.data_prova else ""} for prova in provas]), 200
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@prova_blueprint.route('/provas/<int:id>', methods=['GET'])
def obter_prova(id):
    try:
        prova = ProvaService.get_prova_by_id(id)
        if prova:
            return jsonify({"id": prova.id, 
                            "titulo": prova.titulo, 
                            "materia_id": prova.materia_id, 
                            "descricao": prova.descricao, 
                            "data": prova.data_prova}), 200
        else:
            return jsonify({"message": "Prova não encontrada"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@prova_blueprint.route('/provas', methods=['POST'])
@jwt_required()
def criar_prova():
    data = request.json
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    data_prova = data.get('data')
    materia_id = data.get('materia_id')

    if not titulo or not materia_id:
        return jsonify({"message": "Campos 'titulo' e 'materia_id' são obrigatórios"}), 400

    try:
        prova = ProvaService.create_prova(titulo, descricao, data_prova, materia_id) 
        return jsonify({"id": prova.id, "titulo": prova.titulo}), 201
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500

@prova_blueprint.route('/provas/<int:id>', methods=['DELETE'])
def deletar_prova(id):
    try:
        success = ProvaService.delete_prova(id)
        if success:
            return jsonify({"message": "Prova deletada com sucesso"}), 200
        else:
            return jsonify({"message": "Prova não encontrada"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500
    
@prova_blueprint.route('/provas/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_prova(id):
    data = request.json
    try:
        user_id = get_jwt_identity()
        prova = ProvaService.get_prova_by_id(id)
        if not prova or prova.user_id != user_id:
            return jsonify({"message": "Prova não encontrada ou acesso negado"}), 404

        prova_atualizada = ProvaService.update_prova(
            prova=prova,
            titulo=data.get('titulo'),
            descricao=data.get('descricao'),
            data=data.get('data'),
            materia_id=data.get('materia_id')
        )

        if prova_atualizada:
            return jsonify({
                "id": prova.id,
                "titulo": prova.titulo,
                "descricao": prova.descricao,
                "data": prova.data_prova.strftime("%Y-%m-%d"),
                "materia_id": prova.materia_id
            }), 200
        else:
            return jsonify({"message": "Falha na atualização"}), 500

    except ValueError as ve:
        return jsonify({"message": f"Formato de data inválido: {ve}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500