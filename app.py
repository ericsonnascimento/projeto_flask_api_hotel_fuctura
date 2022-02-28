from flask import Flask
from flask_restful import Api, Resource, reqparse

# instalando aplicação através da classe Flask
app = Flask(__name__)  # dunder name
api = Api(app)

HOTEIS = [
    {
        "hotel_id": "ibis",
        "nome": "IBIS",
        "cidade": "Olinda",
        "diaria": 150,
        "estrelas": 3,
    },
    {
        "hotel_id": "delmar",
        "nome": "Delmar Hotel",
        "cidade": "Aracaju",
        "diaria": 210,
        "estrelas": 4,
    },
]

class Hoteis(Resource): #GET ALL
    def get(self):
        return {"Hoteis": HOTEIS}, 200

class Hotel(Resource):
    def get(self, hotel_id): #GET (POR HOTEL)
        for c in HOTEIS:
            if c["hotel_id"] == hotel_id:
                return c, 200
        return "Hotel nao encontrado", 404

    def post(self, hotel_id): #POST
        '''
        Metodo responsavel por tratar a requisição POST feita ao API
        :param hotel_id: ID do Hotel a ser inserido
        :return: Sucesso caso o hotel não seja inserido e sonsiga ser inserido na base de dados
        '''
        '''for p in HOTEIS:
            if p['hotel_id'] == hotel_id:
                return {'mensagem': f'Hotel {hotel_id} já existe'}, 409
'''
        parser = reqparse.RequestParser() # interpretador da requisição
        parser.add_argument('nome', required=True, type=str)
        parser.add_argument('cidade', required=True, type=str)
        parser.add_argument('estrelas', required=True, type=int)
        parser.add_argument('diaria', required=True, type=float)

        dados = parser.parse_args()

        dados['hotel_id'] = hotel_id
        HOTEIS.append(dados)
        return {'mensagem': 'Hotel adicionado com sucesso'}, 201

    def delete(self, hotel_id): #DELETAR
        hotel_encontrado = None

        for d in HOTEIS:
            if d['hotel_id'] == hotel_id:
                hotel_encontrado = d
                break
        if not hotel_encontrado:
            return {'mensagem': f'Hotel com {hotel_id} não encontrado!'}, 404

        HOTEIS.remove(hotel_encontrado)

        return '', 204

    def put(self, hotel_id): #SUBSTITUIR
        hotel_encontrado = None

        for d in HOTEIS:
            if d['hotel_id'] == hotel_id:
                hotel_encontrado = d
                break
        if not hotel_encontrado:
            return {'mensagem': f'Hotel com {hotel_id} não encontrado!'}, 404

        parser = reqparse.RequestParser()  # interpretador da requisição
        parser.add_argument('nome', required=True, type=str)
        parser.add_argument('cidade', required=True, type=str)
        parser.add_argument('estrelas', required=True, type=int)
        parser.add_argument('diaria', required=True, type=float)

        dados = parser.parse_args()

        dados['hotel_id'] = hotel_id
        for d in HOTEIS:
            if d['hotel_id'] == hotel_id:
                d['nome'] = dados['nome']
                d['cidade'] = dados['cidade']
                d['estrelas'] = dados['estrelas']
                d['diaria'] = dados['diaria']

        return {'mensagem': f'Hotel {hotel_id} substituido com sucesso!'}, 201

api.add_resource(Hoteis, "/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")

if __name__ == "__main__":
    # Executando aplicação
    app.run(debug=True)
