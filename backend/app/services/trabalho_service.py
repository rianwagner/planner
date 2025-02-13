from ..models.trabalho_model import Trabalho
from ..repositories.trabalho_repository import TrabalhoRepository

class TrabalhoService:
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
    def create_trabalho(titulo, descricao, data_entrega, materia_id):
        if not titulo or not materia_id:
            raise ValueError("Campos 'titulo' e 'materia_id' são obrigatórios")
        try:
            novo_trabalho = Trabalho(titulo=titulo, descricao=descricao, data_entrega=data_entrega, materia_id=materia_id)
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