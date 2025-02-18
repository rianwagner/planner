from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.relatorio_service import RelatorioService
from datetime import datetime

relatorio_blueprint = Blueprint('relatorio', __name__)

@relatorio_blueprint.route('/relatorio', methods=['GET'])
@jwt_required()
def gerar_relatorio():
    try:
        user_id = get_jwt_identity()
        data_inicio_str = request.args.get('data_inicio')
        data_fim_str = request.args.get('data_fim')
        data_inicio = None
        data_fim = None
        if data_inicio_str:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        if data_fim_str:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        relatorio = RelatorioService.gerar_relatorio_por_materia(user_id, data_inicio, data_fim)
        
        return jsonify({
            "success": True,
            "relatorio": relatorio
        }), 200
        
    except ValueError as ve:
        return jsonify({
            "success": False,
            "message": "Formato de data inválido. Use YYYY-MM-DD"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500