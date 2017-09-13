from rotas import db
 
class Rotas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origem = db.Column(db.String(100))
    destino = db.Column(db.String(100))
    distancia = db.Column(db.Float(asdecimal=True))
 
    def __init__(self, origem, destino, distancia):
        self.origem = origem
        self.destino = destino
        self.distancia = distancia
 
    def __repr__(self):
        return '<Rota %d>' % self.id