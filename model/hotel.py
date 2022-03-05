class HotelModel:
    def __init__(self, hotel_id, nome, cidade, estrelas, diaria):
        self.nome = nome
        self.hotel_id = hotel_id
        self.cidade = cidade
        self.estrelas = estrelas
        self.diaria = diaria

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
    HotelModel('delmar', 'Delmar Hotel', 'Aracaju', 4, 210.00),
]
