from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.auth_controller import login, register
from app.controllers.materia_controller import listar_materias, obter_materia, criar_materia, deletar_materia, atualizar_materia
from app.controllers.trabalho_controller import listar_trabalhos, obter_trabalho, criar_trabalho, deletar_trabalho, atualizar_trabalho
from app.controllers.prova_controller import listar_provas, obter_prova, criar_prova, deletar_prova, atualizar_prova
from config import Config
from app import db, create_app
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

app = create_app()
app.config.from_object(Config)
jwt = JWTManager(app)

app.add_url_rule('/login', 'login', login, methods=['POST'])
app.add_url_rule('/register', 'register', register, methods=['POST'])

app.add_url_rule('/materias', 'get_all_materias', listar_materias, methods=['GET'])
app.add_url_rule('/materias/<int:id>', 'get_materia', obter_materia, methods=['GET'])
app.add_url_rule('/materias', 'create_materia', criar_materia, methods=['POST'])
app.add_url_rule('/materias/<int:id>', 'delete_materia', deletar_materia, methods=['DELETE'])
app.add_url_rule('/materias/<int:id>', 'update_materia', atualizar_materia, methods=['PUT'])

app.add_url_rule('/trabalhos', 'get_all_trabalhos', listar_trabalhos, methods=['GET'])
app.add_url_rule('/trabalhos/<int:id>', 'get_trabalho', obter_trabalho, methods=['GET'])
app.add_url_rule('/trabalhos', 'create_trabalho', criar_trabalho, methods=['POST'])
app.add_url_rule('/trabalhos/<int:id>', 'delete_trabalho', deletar_trabalho, methods=['DELETE'])
app.add_url_rule('/trabalhos/<int:id>', 'update_trabalho', atualizar_trabalho, methods=['PUT'])

app.add_url_rule('/provas', 'get_all_prova', listar_provas, methods=['GET'])
app.add_url_rule('/provas/<int:id>', 'get_prova', obter_prova, methods=['GET'])
app.add_url_rule('/provas', 'create_prova', criar_prova, methods=['POST'])
app.add_url_rule('/provas/<int:id>', 'delete_prova', deletar_prova, methods=['DELETE'])
app.add_url_rule('/provas/<int:id>', 'update_prova', atualizar_prova, methods=['PUT'])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

