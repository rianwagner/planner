from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from ..repositories.user_repository import UserRepository
from ..models.user_model import User

class AuthService:
    @staticmethod
    def login(username, password):
        try:
            user = UserRepository.get_by_username(username)
            if user and check_password_hash(user.password, password):
                token = create_access_token(identity=user.id)
                return token
            return None 
        except Exception as e:
            print(f"Erro durante o login: {e}")
            return None
    
    @staticmethod
    def register(username, password):
        try:
            existing_user = UserRepository.get_by_username(username)
            if existing_user:
                return {"error": "Username já existe"}, 400

            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)

            UserRepository.save(new_user)

            return {"message": "Usuário registrado com sucesso!"}, 201
        except Exception as e:
            print(f"Erro durante o registro: {e}")
            return {"error": "Ocorreu um erro durante o registro"}, 500