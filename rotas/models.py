from rotas import db

class Rotas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    rotas = db.Column(db.String(9999))

    def __init__(self, nome, rotas):
        self.nome = nome
        self.rotas = rotas

    def __repr__(self):
        return '<Mapa %d>' % self.id
