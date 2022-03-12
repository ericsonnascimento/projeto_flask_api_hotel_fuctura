from flask import Flask
from flask_restful import Api
from resources.hotel import HoteisResource, HotelResource
from model.sql_alchemy import db

"""
    Instanciando a aplicação através da classe Flask
"""

app = Flask(__name__)  # dunder name
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
api = Api(app)

api.add_resource(HoteisResource, "/hoteis")
api.add_resource(HotelResource, "/hoteis/<string:hotel_id>")  # enpoint

@app.before_first_request
def criar_banco():
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    # Excutando a aplicação
    app.run(debug=True)


