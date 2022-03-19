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

get_all_parser = reqparse.RequestParser()
get_all_parser.add_argument("page", type=int, location="args")
get_all_parser.add_argument("limit", type=int, location="args")

class HoteisResource(Resource):
    def get(self):  # GET ALL
        pagination_data = get_all_parser.parse_args()
        page = pagination_data['page'] or 1
        limit = pagination_data['limit'] or 10
        pagination = HotelModel.query.paginate(page, limit)
        hoteis = [h.to_dict() for h in pagination.items]
        data = { 'hoteis': hoteis,
                 'pages': pagination.page,
                 'total': pagination.total,
                 'limit': limit,
                 }
        if pagination.has_next:
            data['next'] = f'/hoteis?page={pagination.next_num}&limit={limit}'
        if pagination.has_prev:
            data['prev'] = f'/hoteis?page={pagination.prev_num}&limit={limit}'

        return data, http_codes.OK_STATUS_CODE

    def post(self):  # POST
        dados = post_parser.parse_args()  # Criado fora do contexto da classe
        novo_hotel = HotelModel(**dados)
        novo_hotel.save_hotel()
        return novo_hotel.to_dict(), http_codes.CREATED_STATUS_CODE


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
        return '', http_codes.OK_STATUS_CODE

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
