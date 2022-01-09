from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from utils.message_helper import help_message_field_blank, database_unknown_error


class Hotels(Resource):
    @staticmethod
    def get():
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}, 200


class Hotel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nome', type=str, required=True, help=help_message_field_blank("nome"))
    parser.add_argument('estrelas', type=float, required=True, help=help_message_field_blank("estrelas"))
    parser.add_argument('diaria', type=float, required=True, help=help_message_field_blank("diaria"))
    parser.add_argument('cidade', type=str, required=True, help=help_message_field_blank("cidade"))

    @staticmethod
    def get(hotel_id):
        try:
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                return hotel.json(), 200
            return {'message': 'Hotel not found'}, 404
        except:
            return database_unknown_error()


    @jwt_required()
    def post(self, hotel_id):
        try:
            if HotelModel.find_hotel(hotel_id):
                return {"message": "Hotel id \'{}\' already exists.".format(hotel_id)}, 400

            dados = self.parser.parse_args()
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 200
        except:
            return database_unknown_error()


    @jwt_required()
    def put(self, hotel_id):
        try:
            dados = self.parser.parse_args()
            saved_hotel = HotelModel.find_hotel(hotel_id)
            if saved_hotel:
                saved_hotel.update_hotel(**dados)
                saved_hotel.save_hotel()
                return saved_hotel.json(), 200
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201
        except:
            database_unknown_error()

    @jwt_required()
    def delete(self, hotel_id):
        try:
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                hotel.delete_hotel()
                return {'message': 'hotel deleted'}, 200
            return {'message': 'Hotel not founded.'}, 404
        except:
            return database_unknown_error()


