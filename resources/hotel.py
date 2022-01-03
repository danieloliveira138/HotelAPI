from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hotels(Resource):
    def get(self):
        return hoteis

hoteis = [
        {
            'hotel_id': 'alpha',
            'nome': 'Alpha Hotel',
            'estrelas': 4.3,
            'diaria': 420.90,
            'cidade': 'Rio de Janeiro'
        },
        {
            'hotel_id': 'bravo',
            'nome': 'Bravo Hotel',
            'estrelas': 4.4,
            'diaria': 290.90,
            'cidade': 'Santa Catarina'
        },
        {
            'hotel_id': 'charlie',
            'nome': 'Charlie Hotel',
            'estrelas': 3.9,
            'diaria': 380.90,
            'cidade': 'São Paulo'
        }
]

class Hotel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nome')
    parser.add_argument('estrelas')
    parser.add_argument('diaria')
    parser.add_argument('cidade')

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found'}, 404

    def post(self, hotel_id):
        dados = self.parser.parse_args()
        new_hotel = HotelModel(hotel_id, **dados)
        
        hoteis.append(new_hotel.json())
        return new_hotel.json(), 200
    
    def put(self, hotel_id):
        dados = self.parser.parse_args()
        new_hotel = HotelModel(hotel_id, **dados)

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(new_hotel.json())
            return new_hotel.json(), 200
        else:
            hoteis.append(new_hotel.json())
            return new_hotel.json(), 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': "Hotel deleted"}, 202

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

