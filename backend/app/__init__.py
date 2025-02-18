from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'segredo'  # Use uma chave segura em produção
    jwt = JWTManager(app)
    CORS(app)
    app.config['SWAGGER'] = {
        'title': 'API Acadêmica',
        'uiversion': 3,
        'specs_route': '/apidocs/',
        'openapi': '3.0.0'
    }
    Swagger(app, template_file='docs/api_docs.yaml')
    app.config.from_object(Config)

    db.init_app(app)
    from app.controllers.auth_controller import auth_blueprint
    from app.controllers.materia_controller import materia_blueprint
    from app.controllers.trabalho_controller import trabalho_blueprint
    from app.controllers.prova_controller import prova_blueprint
    from app.controllers.relatorio_controller import relatorio_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(materia_blueprint, url_prefix='/api')
    app.register_blueprint(trabalho_blueprint, url_prefix='/api')
    app.register_blueprint(prova_blueprint, url_prefix='/api')
    app.register_blueprint(relatorio_blueprint, url_prefix='/api')

    return app