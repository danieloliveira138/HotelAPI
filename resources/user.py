import flask
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.constans import LOGIN_FIELD, PASSWD_FIELD
from blacklist import BLACKLIST
from utils.message_helper import help_message_field_blank, database_unknown_error


def get_login_args():
    attributes = reqparse.RequestParser()
    attributes.add_argument(LOGIN_FIELD, type=str, required=True, help=help_message_field_blank(LOGIN_FIELD))
    attributes.add_argument(PASSWD_FIELD, type=str, required=True, help=help_message_field_blank(PASSWD_FIELD))
    return attributes.parse_args()


class User(Resource):
    @jwt_required()
    def get(self, user_id):
        try:
            user = UserModel.find_user(user_id=user_id)
            if user:
                return user.json(), 200
            return {'message': 'User not funded.'}, 404
        except:
            return database_unknown_error()

    @jwt_required()
    def delete(self, user_id):
        try:
            user = UserModel.find_user(user_id=user_id)
            if user:
                user.delete_user()
                return {'message': 'User deleted.'}, 200
            return {'message': 'User not found.'}, 404
        except:
            return database_unknown_error()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            data = get_login_args()
            if UserModel.find_by_login(data[LOGIN_FIELD]):
                return {'message': "The login \'{}\' already exists".format(data[LOGIN_FIELD])}, 500

            user = UserModel(**data)
            user.save_user()
            return {'message': 'User created successfully!'}, 201
        except:
            return database_unknown_error()


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            data = get_login_args()
            user = UserModel.find_by_login(data[LOGIN_FIELD])
            if user and safe_str_cmp(user.passwd, data[PASSWD_FIELD]):
                access_token = create_access_token(identity=user.user_id)
                response = flask.make_response({'message': 'Login success'})
                response.headers.add('access_token', access_token)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            return {'message': 'The username or password is incorrect.'}, 401
        except:
            return database_unknown_error()


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        try:
            jwt_id = get_jwt()['jti']
            BLACKLIST.add(jwt_id)
            return {'message': 'Logged out successfully!'}, 200
        except:
            database_unknown_error()
