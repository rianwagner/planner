from ..models.prova_model import Prova
from ..repositories.prova_repository import ProvaRepository
from flask_jwt_extended import get_jwt_identity
from datetime import datetime

class ProvaService:

    @staticmethod
    def get_provas_by_user(user_id):
        return Prova.query.filter_by(user_id=user_id).all()
    @staticmethod
    def get_all_provas():
        try:
            return ProvaRepository.get_all()
        except Exception as e:
            print(f"Erro ao buscar provas: {e}")
            return []

    @staticmethod
    def get_prova_by_id(id):
        try:
            return ProvaRepository.get_by_id(id)
        except Exception as e:
            print(f"Erro ao buscar prova por ID: {e}")
            return None

    @staticmethod
    def create_prova(titulo, descricao, data, materia_id):
        if not titulo or not materia_id:
            raise ValueError("Campos 'titulo' e 'materia_id' são obrigatórios")
        try:
            user_id = get_jwt_identity()
            data_prova = datetime.strptime(data, '%Y-%m-%d').date()
            nova_prova = Prova(titulo=titulo, descricao=descricao, data_prova=data_prova, materia_id=materia_id, user_id=user_id)
            return ProvaRepository.save(nova_prova)
        except ValueError as ve:
            print(f"Formato de data inválido: {ve}")
            raise ValueError("Data deve estar no formato 'YYYY-MM-DD'")
        except Exception as e:
            print(f"Erro ao criar prova: {e}")
            return None

    @staticmethod
    def delete_prova(id):
        try:
            return ProvaRepository.delete(id)
        except Exception as e:
            print(f"Erro ao deletar prova: {e}")
            return False
    @staticmethod
    def update_prova(prova, titulo, descricao, data, materia_id):
        try:
            prova.titulo = titulo
            prova.descricao = descricao
            if isinstance(data, str):
                if 'T' in data:
                    data = datetime.fromisoformat(data).date()
                else:
                    data = datetime.strptime(data, '%Y-%m-%d').date()
            prova.data_prova = data
            prova.materia_id = materia_id
            return ProvaRepository.save(prova)
        except Exception as e:
            print(f"Erro ao atualizar prova: {e}")
            return None