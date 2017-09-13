from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from rotas import db, app
from rotas.models import Rotas
from rotas.dijkstra import dijkstra, adequar_rotas
rotas = Blueprint('rota', __name__)


@rotas.route('/')
@rotas.route('/home')
def home():
    return "Rotas"


@rotas.route('/cheapest')
def cheapest():
    '''
    Essa função calcula a melhor rota com o menor custo para um dado mapa.
    Os dados de entrada sao:
    mapa (Nome do mapa)
    origem (Local de origem)
    destino (Local de destino)
    autonomia (Autonomia do veículo em km/l)
    valor_combustivel (Valor do litro do combustível)
    '''
    mapa = request.args.get('mapa')
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    autonomia = request.args.get('autonomia')
    valor_combustivel = request.args.get('combustivel')
    rota = Rotas.query.filter_by(nome=mapa).first()
    adequada = adequar_rotas(rota.rotas)
    melhor_caminho, menor_km = dijkstra(adequada, origem, destino)
    litros = float(menor_km) / float(autonomia)
    custo = float(litros) * float(valor_combustivel)
    return "Rota %s com custo %s" % (str(melhor_caminho), str(custo))


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
        '''
        Insere uma nova malha logistica no banco de dados.
        Deve ser passado um objeto JSON no formato:
        {
           "nome": "<NOME_DO_MAPA>",
           "rotas": "[{'destino': 'B', 'origem': 'A', 'distancia': '10'},
                      {'destino': 'D', 'origem': 'B', 'distancia': '15'}]
        }
        '''
        dados = request.json
        rota = Rotas(dados['nome'], dados['rotas'])
        db.session.add(rota)
        db.session.commit()
        return jsonify({rota.id: {
            'nome': rota.nome,
            'rotas': str(rota.rotas),
        }})

    def put(self, id):
        return None

    def delete(self, id):
        return None


rotas_view = RotasView.as_view('rotas_view')
app.add_url_rule(
    '/rotas', view_func=rotas_view, methods=['GET', 'POST']
)
app.add_url_rule(
    '/rotas/', view_func=rotas_view, methods=['GET', 'POST']
)
