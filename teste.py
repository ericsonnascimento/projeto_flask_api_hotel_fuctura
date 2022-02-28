from flask import Flask
from flask_restful import Api, Resource, reqparse

# instalando aplicação através da classe Flask
app = Flask(__name__)  # dunder name

@app.route('/')
def index():
    return 'Teste'

@app.route('/hello')
def hello():
    return 'Hello, World'

if __name__ == "__main__":
    # Executando aplicação
    app.run(debug=True)