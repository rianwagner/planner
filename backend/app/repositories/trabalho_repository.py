from ..models.trabalho_model import Trabalho
from .. import db
from sqlalchemy.exc import SQLAlchemyError

class TrabalhoRepository:
    @staticmethod
    def get_all():
        try:
            return Trabalho.query.all()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar todos os trabalhos: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        try:
            return Trabalho.query.get(id)
        except SQLAlchemyError as e:
            print(f"Erro ao buscar trabalho por ID: {e}")
            return None

    @staticmethod
    def save(trabalho):
        try:
            db.session.add(trabalho)
            db.session.commit()
            return trabalho
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao salvar trabalho: {e}")
            return None

    @staticmethod
    def delete(id):
        try:
            trabalho = Trabalho.query.get(id)
            if trabalho:
                db.session.delete(trabalho)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao deletar trabalho: {e}")
            return False