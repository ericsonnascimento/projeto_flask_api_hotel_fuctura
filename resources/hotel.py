from flask_restful import Resource, reqparse
from model.hotel import HOTEIS, HotelModel
import resources.http_status_code as http_code

# Interpretador da requisição
post_parser = reqparse.RequestParser(bundle_errors=True)
post_parser.add_argument("nome", required=True, type=str)
post_parser.add_argument("cidade", required=True, type=str)
post_parser.add_argument("estrelas", required=True, type=int)
post_parser.add_argument("diaria", required=True, type=float)

# Interpretador da requisição
put_parser = reqparse.RequestParser(bundle_errors=True)
put_parser.add_argument("nome", required=False, type=str)
put_parser.add_argument("cidade", required=False, type=str)
put_parser.add_argument("estrelas", required=False, type=int)
put_parser.add_argument("diaria", required=False, type=float)


class HoteisResource(Resource):
    def get(self):  # GET ALL
        hotel_dict = [h.to_dict() for h in HOTEIS]
        return {"hoteis": hotel_dict}, http_code.OK_STATUS_CODE


class HotelResource(Resource):
    def get(self, hotel_id):  # GET
        for hotel in HOTEIS:
            if hotel.hotel_id == hotel_id:
                return hotel.to_dict(), http_code.OK_STATUS_CODE  # Tupla

        return "HotelResource não encontrado", http_code.NOT_FOUND_STATUS_CODE

    def post(self, hotel_id):  # POST
        """
            Método responsável por tratar a requisição POST feita a API.

        :param hotel_id: Id do hotel a ser inserido
        :return: Sucesso caso o o id do hotel não exista e consiga ser inserido na base de dados
        """

        # Código de conflito: 409

        for h in HOTEIS:
            if h.hotel_id == hotel_id:
                return {"mensagem": f"HotelResource com id {hotel_id} já existe!"}, http_code.CONFLIT_STATUS_CODE

        dados = post_parser.parse_args()

        novo_hotel = HotelModel(
            hotel_id=hotel_id,
            nome=dados["nome"],
            estrelas=dados["estrelas"],
            cidade=dados["cidade"],
            diaria=dados["diaria"],
        )

        HOTEIS.append(novo_hotel)
        return {"mensagem": "HotelResource adicionado com sucesso"}, http_code.CREATED_STATUS_CODE

    def delete(self, hotel_id):
        hotel_encontrado = None

        for h in HOTEIS:
            if h.hotel_id == hotel_id:
                hotel_encontrado = h
                break

        if not hotel_encontrado:
            return {"message:" f"HotelResource com id {hotel_id} não encontrado"}

        HOTEIS.remove(hotel_encontrado)

        return "", http_code.NO_CONTENT_STATUS_CODE

    def put(self, hotel_id):

        dados = put_parser.parse_args()

        for hotel in HOTEIS:
            if hotel.hotel_id == hotel_id:
                hotel.nome = dados["nome"] or hotel.nome
                hotel.cidade = dados["cidade"] or hotel.cidade
                hotel.diaria = dados["diaria"] or hotel.diaria
                hotel.estrelas = dados["estrelas"] or hotel.estrelas
                return hotel.to_dict(), http_code.CREATED_STATUS_CODE

        return {"message": f"HotelResource com id '{hotel_id}' não foi encontrado"}, http_code.NOT_FOUND_STATUS_CODE