from .. import db

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    trabalhos = db.relationship('Trabalho', backref='materia', lazy=True)
    provas = db.relationship('Prova', backref='materia', lazy=True)