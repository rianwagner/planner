from .. import db

class Prova(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    materia_id = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)