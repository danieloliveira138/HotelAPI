import sqlite3
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.site import SiteModel
from flask_jwt_extended import jwt_required
from utils.message_helper import help_message_field_blank, database_unknown_error
from utils.filters import normalize_dictionary
from resources.hotel_filtes import normalize_path_params, hotels_query


class Hotels(Resource):
    path_params = reqparse.RequestParser()
    path_params.add_argument('estrelas_min', type=float)
    path_params.add_argument('estrelas_max', type=float)
    path_params.add_argument('diaria_min', type=float)
    path_params.add_argument('diaria_max', type=float)
    path_params.add_argument('limit', type=int)
    path_params.add_argument('offset', type=int)
    path_params.add_argument('cidade', type=str)

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        args = self.path_params.parse_args()
        valid_args = normalize_dictionary(args)
        parameters = normalize_path_params(**valid_args)

        query = hotels_query(with_city=parameters.get('cidade') is not None)
        values = tuple([parameters[key] for key in parameters])
        result = cursor.execute(query, values)

        hotels = []
        for row in result:
            hotels.append({
                'hotel_id': row[0],
                'nome': row[1],
                'estrelas': row[2],
                'diaria': row[3],
                'cidade': row[4],
                'site:': row[5]
            })
        return hotels, 200


class Hotel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nome', type=str, required=True, help=help_message_field_blank("nome"))
    parser.add_argument('estrelas', type=float, required=True, help=help_message_field_blank("estrelas"))
    parser.add_argument('diaria', type=float, required=True, help=help_message_field_blank("diaria"))
    parser.add_argument('cidade', type=str, required=True, help=help_message_field_blank("cidade"))
    parser.add_argument('site_id', type=int, required=True, help=help_message_field_blank("site_id"))

    @staticmethod
    def get(hotel_id):
        try:
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                return hotel.json(), 200
            return {'message': 'Hotel not found'}, 404
        except NameError:
            return database_unknown_error(NameError.name)

    @jwt_required()
    def post(self, hotel_id):
        try:
            if HotelModel.find_hotel(hotel_id):
                return {"message": "Hotel id \'{}\' already exists.".format(hotel_id)}, 400

            dados = self.parser.parse_args()

            if not SiteModel.find_by_id(dados.get('site_id')):
                return {'message': 'The field site_id is non related a valid site, check that field'}
            hotel = HotelModel(hotel_id, **dados)

            hotel.save_hotel()
            return hotel.json(), 200
        except NameError:
            return database_unknown_error(NameError.name)

    @jwt_required()
    def put(self, hotel_id):
        try:
            dados = self.parser.parse_args()
            saved_hotel = HotelModel.find_hotel(hotel_id)
            if not SiteModel.find_by_id(dados.get('site_id')):
                return {'message': 'The field site_id is non related a valid site, check that field'}
            if saved_hotel:
                saved_hotel.update_hotel(**dados)
                saved_hotel.save_hotel()
                return saved_hotel.json(), 200
            hotel = HotelModel(hotel_id, **dados)
            hotel.save_hotel()
            return hotel.json(), 201
        except NameError:
            database_unknown_error(NameError.name)

    @jwt_required()
    def delete(self, hotel_id):
        try:
            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                hotel.delete_hotel()
                return {'message': 'hotel deleted'}, 200
            return {'message': 'Hotel not founded.'}, 404
        except NameError:
            return database_unknown_error(NameError.name)
