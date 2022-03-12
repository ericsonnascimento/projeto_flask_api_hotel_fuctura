from model.sql_alchemy import db



class HotelModel(db.Model):
    __tabela__ = 'hoteis'
    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    estrelas = db.Column(db.Integer, nullable=False)
    diaria = db.Column(db.Float(precision=2), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.get(hotel_id)
        return None if not hotel else hotel

    def update_hotel(self, **dados):
        self.nome = dados["nome"] or self.nome
        self.estrelas = dados["estrelas"] or self.estrelas
        self.diaria = dados["diaria"] or self.diaria
        self.cidade = dados["cidade"] or self.cidade

        #key_error

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()  # Confirmando a transação

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'cidade': self.cidade,
            'estrelas': self.estrelas,
            'diaria': self.diaria
        }

HOTEIS = [
    HotelModel('ibis', 'IBIS', 'Olinda', 4, 150.00),
    HotelModel('delmar', 'Delmar HotelResource', 'Aracaju', 4, 210.00),
]
