from flask import request, jsonify, Blueprint
from ..services.trabalho_service import TrabalhoService
from ..repositories.trabalho_repository import TrabalhoRepository
from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

trabalho_blueprint = Blueprint('trabalho', __name__)

@trabalho_blueprint.route('/trabalhos', methods=['GET'])
@jwt_required()
def listar_trabalhos():
    try:
        user_id = get_jwt_identity()
        trabalhos = TrabalhoService.get_trabalhos_by_user(user_id) 
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
@jwt_required()
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
            data_entrega = datetime.fromisoformat(data_entrega)
        user_id = get_jwt_identity()
        trabalho = TrabalhoService.create_trabalho(
            titulo=titulo, 
            descricao=descricao, 
            data_entrega=data_entrega, 
            materia_id=materia_id, 
            user_id=user_id
            )
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
@jwt_required()
def deletar_trabalho(id):
    try:
        success = TrabalhoService.delete_trabalho(id)
        if success:
            return jsonify({"message": "Trabalho deletado com sucesso"}), 200
        else:
            return jsonify({"message": "Trabalho não encontrado"}), 404
    except Exception as e:
        return jsonify({"message": "Erro interno no servidor"}), 500
    
@trabalho_blueprint.route('/trabalhos/<int:id>', methods=['PUT'])
@jwt_required()
def atualizar_trabalho(id):
    data = request.json
    try:
        user_id = get_jwt_identity()
        trabalho = TrabalhoService.get_trabalho_by_id(id)
        if not trabalho or trabalho.user_id != user_id:
            return jsonify({"message": "Trabalho não encontrado ou acesso negado"}), 404
        
        data_entrega_str = data.get('data_entrega')
        if not data_entrega_str.endswith('T00:00:00'):
            data_entrega_str += 'T00:00:00'
        nova_data = datetime.fromisoformat(data_entrega_str)

        trabalho_atualizado = TrabalhoService.update_trabalho(
            trabalho=trabalho,
            titulo=data.get('titulo'),
            descricao=data.get('descricao'),
            data_entrega=nova_data,
            materia_id=data.get('materia_id')
        )

        if trabalho_atualizado:
            return jsonify({
                "id": trabalho.id,
                "titulo": trabalho.titulo,
                "descricao": trabalho.descricao,
                "data_entrega": trabalho.data_entrega.isoformat(),
                "materia_id": trabalho.materia_id
            }), 200
        else:
            return jsonify({"message": "Falha na atualização"}), 500

    except ValueError as ve:
        return jsonify({"message": f"Formato de data inválido: {ve}"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500