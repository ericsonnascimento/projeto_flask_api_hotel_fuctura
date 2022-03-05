from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

"""
    Instanciando a aplicação através da classe Flask
"""

app = Flask(__name__)  # dunder name
api = Api(app)

api.add_resource(Hoteis, "/hoteis")
api.add_resource(Hotel, "/hoteis/<string:hotel_id>")  # enpoint

if __name__ == "__main__":
    # Excutando a aplicação
    app.run(debug=True)
