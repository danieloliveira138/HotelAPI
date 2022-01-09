from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hotels(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}, 200


def message_required_field(field_name: str):
    return "Field \'{}\' must not be empty".format(field_name)


class Hotel(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('nome', type=str, required=True, help=message_required_field("nome"))
    parser.add_argument('estrelas', type=float, required=True, help=message_required_field("estrelas"))
    parser.add_argument('diaria', type=float, required=True, help=message_required_field("diaria"))
    parser.add_argument('cidade', type=str, required=True, help=message_required_field("cidade"))

    def get(self, hotel_id):
        try:
            hotel = HotelModel.find_hotel(hotel_id)
        except:
            return {'message': "An error ocurred trying to list hotels."}, 500
        finally:
            if hotel:
                return hotel.json(), 200
            return {'message': 'Hotel not found'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id \'{}\' already exists.".format(hotel_id)}, 400

        dados = self.parser.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': "An error ocurred trying to create hotel."}, 500
        finally:
            return hotel.json(), 200

    @jwt_required()
    def put(self, hotel_id):
        dados = self.parser.parse_args()
        saved_hotel = HotelModel.find_hotel(hotel_id)
        if saved_hotel:
            saved_hotel.update_hotel(**dados)
            saved_hotel.save_hotel()
            return saved_hotel.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': "An error ocurred trying to update hotel."}, 500
        finally:
            return hotel.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': "An error ocurred trying to delete hotel."}, 500
            finally:
                return {'message': 'hotel deleted'}, 200
        return {'message': 'Hotel not founded.'}, 404
