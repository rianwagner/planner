from ..models.materia_model import Materia
from .. import db
from sqlalchemy.exc import SQLAlchemyError

class MateriaRepository:
    @staticmethod
    def get_all():
        try:
            return Materia.query.all()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar todas as matérias: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        try:
            return Materia.query.get(id)
        except SQLAlchemyError as e:
            print(f"Erro ao buscar matéria por ID: {e}")
            return None

    @staticmethod
    def save(materia):
        try:
            db.session.add(materia)
            db.session.commit()
            return materia
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao salvar matéria: {e}")
            return None

    @staticmethod
    def delete(id):
        try:
            materia = Materia.query.get(id)
            if materia:
                db.session.delete(materia)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao deletar matéria: {e}")
            return False