from model.sql_alchemy import bd


class HotelModel(bd.Model):
    __tablename__ = "hoteis"  # Mapeamento da tabela
    hotel_id = bd.Column(bd.String, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False)
    estrelas = bd.Column(bd.SmallInteger, nullable=False)
    diaria = bd.Column(bd.Float(precision=2), nullable=False)
    cidade = bd.Column(bd.String(40), nullable=False)

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.get(hotel_id)
        return None if not hotel else hotel

    def update_hotel(self, **dados):
        self.nome = dados["nome"] or self.nome
        self.estrelas = dados["estrelas"] or self.estrelas
        self.diaria = dados["diaria"] or self.diaria
        self.cidade = dados["cidade"] or self.cidade

    def delete(self):
        bd.session.delete(self)
        bd.session.commit()

    def save_hotel(self):
        bd.session.add(self)
        bd.session.commit()

    def to_dict(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "cidade": self.cidade,
            "estrelas": self.estrelas,
            "diaria": self.diaria,
        }
