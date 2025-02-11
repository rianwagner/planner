from ..models.prova_model import Prova
from ..repositories.prova_repository import ProvaRepository

class ProvaService:
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
            nova_prova = Prova(titulo=titulo, descricao=descricao, data=data, materia_id=materia_id)
            return ProvaRepository.save(nova_prova)
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