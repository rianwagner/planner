from .. import db

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    titulo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_prova = db.Column(db.Date, nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False) 