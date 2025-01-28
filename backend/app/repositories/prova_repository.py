from ..models.prova_model import Prova
from .. import db
from sqlalchemy.exc import SQLAlchemyError

class ProvaRepository:
    @staticmethod
    def get_all():
        try:
            return Prova.query.all()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar todas as provas: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        try:
            return Prova.query.get(id)
        except SQLAlchemyError as e:
            print(f"Erro ao buscar prova por ID: {e}")
            return None

    @staticmethod
    def save(prova):
        try:
            db.session.add(prova)
            db.session.commit()
            return prova
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao salvar prova: {e}")
            return None

    @staticmethod
    def delete(id):
        try:
            prova = Prova.query.get(id)
            if prova:
                db.session.delete(prova)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao deletar prova: {e}")
            return False