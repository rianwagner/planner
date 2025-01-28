from ..models.user_model import User
from .. import db
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    @staticmethod
    def get_all():
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar todos os usuários: {e}")
            return []

    @staticmethod
    def get_by_id(id):
        try:
            return User.query.get(id)
        except SQLAlchemyError as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            return None

    @staticmethod
    def get_by_username(username):
        try:
            return User.query.filter_by(username=username).first()
        except SQLAlchemyError as e:
            print(f"Erro ao buscar usuário por username: {e}")
            return None

    @staticmethod
    def save(user):
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao salvar usuário: {e}")
            return None

    @staticmethod
    def delete(id):
        try:
            user = User.query.get(id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Erro ao deletar usuário: {e}")
            return False