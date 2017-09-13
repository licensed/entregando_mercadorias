import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from rotas import db, app
from rotas.models import Rotas
from dijkstra import dijkstra, adequar_rotas
from ast import literal_eval
rotas = Blueprint('rota', __name__)


@rotas.route('/')
@rotas.route('/home')
def home():
    return "Rotas"

@rotas.route('/cheapest')
def cheapest():
    mapa = request.args.get('mapa')
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    autonomia = request.args.get('autonomia')
    valor_combustivel = request.args.get('combustivel')
    rota = Rotas.query.filter_by(nome=mapa).first()
    adequada = adequar_rotas(rota.rotas)
    melhor_caminho, menor_km = dijkstra(adequada, origem, destino)
    litros = float(menor_km)/float(autonomia)
    custo = float(litros) * float(valor_combustivel)
    return "Rota %s com custo %s" % (str(melhor_caminho), str(custo))
    #adequada = adequar_rotas(rota.rotas)
    #print type(adequada)
    #dijkstra = Dijkstra(adequada,origem,destino)
    #return "Lowest: ", dijkstra.get_lowest()

class RotasView(MethodView):

    def get(self, id=None, page=1):
        if not id:
            rotas = Rotas.query.paginate(page, 10).items
            res = {}
            for rota in rotas:
                res[rota.id] = {
                    'nome': rota.nome,
                    'rotas': str(rota.rotas),
                }
        else:
            rota = Rotas.query.filter_by(id=id).first()
            if not rota:
                abort(404)
            res = {
                    'nome': rota.nome,
                    'rotas': str(rota.rotas),
            }
        return jsonify(res)

    def post(self):
        dados = request.json
        rota = Rotas(dados['nome'], dados['rotas'])
        db.session.add(rota)
        db.session.commit()
        return jsonify({rota.id: {
                    'nome': rota.nome,
                    'rotas': str(rota.rotas),
        }})

    def put(self, id):
        return

    def delete(self, id):
        return

rotas_view = RotasView.as_view('rotas_view')
app.add_url_rule(
    '/rotas', view_func=rotas_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/rotas/', view_func=rotas_view, methods=['GET', 'POST']
)
#app.add_url_rule(
#    '/rotas/<int:id>', view_func=rotas_view, methods=['GET']
#)
