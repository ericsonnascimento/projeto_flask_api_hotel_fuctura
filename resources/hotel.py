from flask_restful import Resource, reqparse
from model.hotel import HOTEIS, HotelModel


class Hoteis(Resource):
    def get(self):  # GET ALL
        hotel_dict = [h.to_dict() for h in HOTEIS]
        return {"hoteis": hotel_dict}, 200


class Hotel(Resource):
    def get(self, hotel_id):  # GET
        for hotel in HOTEIS:
            if hotel.hotel_id == hotel_id:
                return hotel.to_dict(), 200  # Tupla

        return "Hotel não encontrado", 404

    def post(self, hotel_id):  # POST
        """
            Método responsável por tratar a requisição POST feita a API.

        :param hotel_id: Id do hotel a ser inserido
        :return: Sucesso caso o o id do hotel não exista e consiga ser inserido na base de dados
        """

        # Código de conflito: 409

        for h in HOTEIS:
            if h.hotel_id == hotel_id:
                return {"mensagem": f"Hotel com id {hotel_id} já existe!"}, 409

        # Interpretador da requisição
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("nome", required=True, type=str)
        parser.add_argument("cidade", required=True, type=str)
        parser.add_argument("estrelas", required=True, type=int)
        parser.add_argument("diaria", required=True, type=float)

        dados = parser.parse_args()

        novo_hotel = HotelModel(
            hotel_id=hotel_id,
            nome=dados["nome"],
            estrelas=dados["estrelas"],
            cidade=dados["cidade"],
            diaria=dados["diaria"],
        )

        HOTEIS.append(novo_hotel)
        return {"mensagem": "Hotel adicionado com sucesso"}, 201

    def delete(self, hotel_id):
        hotel_encontrado = None

        for h in HOTEIS:
            if h.hotel_id == hotel_id:
                hotel_encontrado = h
                break

        if not hotel_encontrado:
            return {"message:" f"Hotel com id {hotel_id} não encontrado"}

        HOTEIS.remove(hotel_encontrado)

        return "", 204

    def put(self, hotel_id):
        # Interpretador da requisição
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument("nome", required=False, type=str)
        parser.add_argument("cidade", required=False, type=str)
        parser.add_argument("estrelas", required=False, type=int)
        parser.add_argument("diaria", required=False, type=float)

        dados = parser.parse_args()

        for hotel in HOTEIS:
            if hotel.hotel_id == hotel_id:
                hotel.nome = dados["nome"] or hotel.nome
                hotel.cidade = dados["cidade"] or hotel.cidade
                hotel.diaria = dados["diaria"] or hotel.diaria
                hotel.estrelas = dados["estrelas"] or hotel.estrelas
                return hotel.to_dict(), 201

        return {"message": f"Hotel com id '{hotel_id}' não foi encontrado"}, 404