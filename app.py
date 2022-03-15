from flask import Flask
from flask_restful import Api
from resources.hotel import HoteisResource, HotelResource
from model.sql_alchemy import bd

"""
    Instanciando a aplicação através da classe Flask
"""
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

api.add_resource(HoteisResource, "/hoteis")
api.add_resource(HotelResource, "/hoteis/<string:hotel_id>")


@app.before_first_request
def criar_banco():
    bd.init_app(app)
    bd.create_all()


if __name__ == "__main__":
    app.run(debug=True)
