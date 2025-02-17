from ..models.materia_model import Materia
from ..repositories.materia_repository import MateriaRepository
from flask_jwt_extended import get_jwt_identity


class MateriaService:

    @staticmethod
    def get_materias_by_user(user_id):
        return Materia.query.filter_by(user_id=user_id).all()
    @staticmethod
    def get_all_materias():
        try:
            return MateriaRepository.get_all()
        except Exception as e:
            print(f"Erro ao buscar matérias: {e}")
            return []

    @staticmethod
    def get_materia_by_id(id):
        try:
            return MateriaRepository.get_by_id(id)
        except Exception as e:
            print(f"Erro ao buscar matéria por ID: {e}")
            return None

    @staticmethod
    def create_materia(nome):
        if not nome:
            raise ValueError("O campo 'nome' é obrigatório")
        try:
            user_id = get_jwt_identity()
            nova_materia = Materia(nome=nome, user_id=user_id)
            return MateriaRepository.save(nova_materia)
        except Exception as e:
            print(f"Erro ao criar matéria: {e}")
            return None

    @staticmethod
    def delete_materia(id):
        try:
            return MateriaRepository.delete(id)
        except Exception as e:
            print(f"Erro ao deletar matéria: {e}")
            return False