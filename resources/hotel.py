import sqlite3

from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
from utils.message_helper import help_message_field_blank, database_unknown_error


class Hotels(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        args = self.get_params_args()
        valid_args = self.get_valid_params_args(args)
        parameters = self.normalize_path_params(**valid_args)

        query = self.get_query(parameters.get('cidade') is not None)
        values = tuple([parameters[key] for key in parameters])
        result = cursor.execute(query, values)

        hotels = []
        for row in result:
            hotels.append({
                'hotel_id': row[0],
                'nome': row[1],
                'estrelas': row[2],
                'diaria': row[3],
                'cidade': row[4]
            })
        return hotels, 200

    @classmethod
    def get_query(cls, with_city: bool):
        return "SELECT * FROM hoteis " \
               "WHERE (estrelas > ? and estrelas < ?) " \
               "and (diaria > ? and diaria < ?) " \
               "{} LIMIT ? OFFSET ?".format("and cidade = ?" if with_city else "")

    @classmethod
    def get_params_args(cls):
        path_params = reqparse.RequestParser()
        path_params.add_argument('estrelas_min', type=float)
        path_params.add_argument('estrelas_max', type=float)
        path_params.add_argument('diaria_min', type=float)
        path_params.add_argument('diaria_max', type=float)
        path_params.add_argument('limit', type=int)
        path_params.add_argument('offset', type=int)
        path_params.add_argument('cidade', type=str)
        return path_params.parse_args()

    @classmethod
    def get_valid_params_args(cls, args):
        return {key: args[key] for key in args if args[key] is not None}

    @classmethod
    def normalize_path_params(cls,
                              estrelas_min=0,
                              estrelas_max=5,
                              diaria_min=0,
                              diaria_max=1000,
                              limit=50,
                              offset=0,
                              cidade=None, **data):
        if not cidade:
            params = {
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'limit': limit,
                'offset': offset
            }
        else:
            params = {
                'estrelas_min': estrelas_min,
                'estrelas_max': estrelas_max,
                'diaria_min': diaria_min,
                'diaria_max': diaria_max,
                'cidade': cidade,
                'limit': limit,
                'offset': offset
            }
        return params


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
