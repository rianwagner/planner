from ..models.trabalho_model import Trabalho
from ..repositories.trabalho_repository import TrabalhoRepository
from flask_jwt_extended import get_jwt_identity

class TrabalhoService:

    @staticmethod
    def get_trabalhos_by_user(user_id):
        return Trabalho.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_all_trabalhos():
        try:
            return TrabalhoRepository.get_all()
        except Exception as e:
            print(f"Erro ao buscar trabalhos: {e}")
            return []

    @staticmethod
    def get_trabalho_by_id(id):
        try:
            return TrabalhoRepository.get_by_id(id)
        except Exception as e:
            print(f"Erro ao buscar trabalho por ID: {e}")
            return None

    @staticmethod
    def create_trabalho(titulo, descricao, data_entrega, materia_id, user_id):  # Adicione user_id
        if not titulo or not materia_id or not user_id:
            raise ValueError("Campos 'titulo', 'materia_id' e 'user_id' são obrigatórios")
        try:
            novo_trabalho = Trabalho(
                titulo=titulo, 
                descricao=descricao, 
                data_entrega=data_entrega, 
                materia_id=materia_id, 
                user_id=user_id
            )
            return TrabalhoRepository.save(novo_trabalho)
        except Exception as e:
            print(f"Erro ao criar trabalho: {e}")
            return None

    @staticmethod
    def delete_trabalho(id):
        try:
            return TrabalhoRepository.delete(id)
        except Exception as e:
            print(f"Erro ao deletar trabalho: {e}")
            return False