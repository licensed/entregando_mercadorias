# entregando_mercadorias
Find cheapest path from A to B. Dijkstra classic Algorithm.

Requirements:
Python 3.x
pip

Usage:
#To add new map
POST /rotas
{
    "nome": "SP",
    "rotas": "[{'destino': 'B', 'origem': 'A', 'distancia': '10'}, {'destino': 'D', 'origem': 'B', 'distancia': '15'}, {'destino': 'C', 'origem': 'A', 'distancia': '20'}, {'destino': 'D', 'origem': 'C', 'distancia': '30'}, {'destino': 'E', 'origem': 'B', 'distancia': '50'}, {'destino': 'E', 'origem': 'D', 'distancia': '30'}]"
}

#To get cousts
GET "http://localhost:5000/cheapest?mapa=SP&origem=A&destino=D&autonomia=10&combustivel=2.5"
