import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from rotas import db, app
from rotas.models import Rotas
 
rotas = Blueprint('rota', __name__)
 
@rotas.route('/')
@rotas.route('/home')
def home():
    return "Rotas"

class RotasView(MethodView):
 
    def get(self, id=None, page=1):
        if not id:
            rotas = Rotas.query.paginate(page, 10).items
            res = {}
            for rota in rotas:
                res[rota.id] = {
                    'origem,': rota.origem,
                    'destino': str(rota.destino),
                    'distancia': str(rota.distancia),
                }
        else:
            rota = Rotas.query.filter_by(id=id).first()
            if not rota:
                abort(404)
            res = {
                    'origem,': rota.origem,
                    'destino': str(rota.destino),
                    'distancia': str(rota.distancia),
            }
        return jsonify(res)
 
    def post(self):
        dados = request.json
        rota = Rotas(dados['origem'], dados['destino'], dados['distancia'])
        db.session.add(rota)
        db.session.commit()
        return jsonify({rota.id: {
                    'origem,': rota.origem,
                    'destino': str(rota.destino),
                    'distancia': str(rota.distancia),
        }})
 
    def put(self, id):
        return
 
    def delete(self, id):
        return
 
 
rotas_view =  RotasView.as_view('rotas_view')
app.add_url_rule(
    '/rotas', view_func=rotas_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/rotas/', view_func=rotas_view, methods=['GET', 'POST']
)
#app.add_url_rule(
#    '/rotas/<int:id>', view_func=rotas_view, methods=['GET']
#)