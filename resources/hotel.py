from flask_restful import Resource, reqparse, abort
from model.hotel import HotelModel
import resources.http_status_code as http_codes

post_parser = reqparse.RequestParser()
put_parser = reqparse.RequestParser()


post_parser.add_argument("nome", required=True, help="O atributo nome é requerido")
post_parser.add_argument(
    "estrelas", required=True, help="O atributo estrelas é requerido"
)
post_parser.add_argument("diaria", required=True, help="O atributo diaria é requerido")
post_parser.add_argument("cidade", required=True, help="O atributo cidade é requerido")

put_parser.add_argument("nome", type=str)
put_parser.add_argument("estrelas", type=int)
put_parser.add_argument("diaria", type=float)
put_parser.add_argument("cidade", type=str)


class HoteisResource(Resource):
    def get(self):  # GET ALL
        hotel_dict = [h.to_dict() for h in HotelModel.query.all()]
        return {"hoteis": hotel_dict}, http_codes.OK_STATUS_CODE


class HotelResource(Resource):
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            abort(
                http_codes.NOT_FOUND_STATUS_CODE,
                description=f"Hotel id '{hotel_id}' não encontrado",
            )

        return hotel.to_dict(), http_codes.OK_STATUS_CODE

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if not hotel:
            abort(
                http_codes.NOT_FOUND_STATUS_CODE,
                description=f"Hotel id '{hotel_id}' não encontrado",
            )

        hotel.delete()
        return {"message": "Excluído com sucesso!"}, http_codes.OK_STATUS_CODE

    def post(self, hotel_id):  # POST
        """
            Método responsável por tratar a requisição POST feita a API.

        :param hotel_id: Id do hotel a ser inserido
        :return: Sucesso caso o o id do hotel não exista e consiga ser inserido na base de dados
        """

        if HotelModel.find_hotel(hotel_id):
            abort(
                http_codes.CONFLIT_STATUS_CODE,
                description=f"Hotel id '{hotel_id}' já existe",
            )

        dados = post_parser.parse_args()  # Criado fora do contexto da classe
        novo_hotel = HotelModel(hotel_id=hotel_id, **dados)
        novo_hotel.save_hotel()
        return {"message": "Adicionado com sucesso!"}, http_codes.CREATED_STATUS_CODE

    def put(self, hotel_id):
        dados = put_parser.parse_args()
        hotel = HotelModel.find_hotel(hotel_id)

        if not hotel:
            abort(
                http_codes.NOT_FOUND_STATUS_CODE,
                description=f"Hotel de id {hotel_id} não encontrado",
            )

        hotel.update_hotel(**dados)
        hotel.save_hotel()
        return hotel.to_dict(), http_codes.CREATED_STATUS_CODE
