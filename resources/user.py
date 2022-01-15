import traceback
import flask
from flask import make_response, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.user import UserModel
from utils.constans import LOGIN_FIELD, PASSWD_FIELD, EMAIL_FIELD
from blacklist import BLACKLIST
from utils.message_helper import help_message_field_blank, database_unknown_error


def get_login_args():
    attributes = reqparse.RequestParser()
    attributes.add_argument(LOGIN_FIELD, type=str, required=True, help=help_message_field_blank(LOGIN_FIELD))
    attributes.add_argument(PASSWD_FIELD, type=str, required=True, help=help_message_field_blank(PASSWD_FIELD))
    attributes.add_argument(EMAIL_FIELD, type=str)
    attributes.add_argument('activated', type=bool, required=False)
    return attributes.parse_args()


class User(Resource):
    def get(self, user_id):
        try:
            user = UserModel.find_user(user_id=user_id)
            if user:
                return user.json(), 200
            return {'message': 'User not funded.'}, 404
        except NameError:
            return database_unknown_error(NameError.name)

    @jwt_required()
    def delete(self, user_id):
        try:
            user = UserModel.find_user(user_id=user_id)
            if user:
                user.delete_user()
                return {'message': 'User deleted.'}, 200
            return {'message': 'User not found.'}, 404
        except NameError:
            return database_unknown_error(NameError.name)


class UserRegister(Resource):
    @classmethod
    def post(cls):
        try:
            data = get_login_args()

            if not data.get(EMAIL_FIELD) or data.get(EMAIL_FIELD) is None:
                return database_unknown_error(EMAIL_FIELD), 400

            if UserModel.find_by_email(data[EMAIL_FIELD]):
                return {'message': "The login e-mai {} already existies.".format(data[EMAIL_FIELD])}

            if UserModel.find_by_login(data[LOGIN_FIELD]):
                return {'message': "The login \'{}\' already exists".format(data[LOGIN_FIELD])}, 500

            user = UserModel(**data)
            user.activated = False
            try:
                user.save_user()
                user.send_confirmation_email()
            except NameError:
                user.delete_user()
                traceback.print_exc()
                return database_unknown_error()
            return {'message': 'User created successfully!'}, 201
        except NameError:
            return database_unknown_error(NameError.name)


class UserLogin(Resource):
    @classmethod
    def post(cls):
        try:
            data = get_login_args()
            user = UserModel.find_by_login(data[LOGIN_FIELD])
            if user and safe_str_cmp(user.passwd, data[PASSWD_FIELD]):
                if user.activated:
                    access_token = create_access_token(identity=user.user_id)
                    response = flask.make_response({'message': 'Login success'})
                    response.status_code = 200
                    response.headers.add('access_token', access_token)
                    response.headers.add('Access-Control-Allow-Origin', '*')
                    return response
                return {'message': 'User not activated.'}, 400
            return {'message': 'The username or password is incorrect.'}, 401
        except NameError:
            return database_unknown_error(NameError.name)


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        try:
            jwt_id = get_jwt()['jti']
            BLACKLIST.add(jwt_id)
            return {'message': 'Logged out successfully!'}, 200
        except NameError:
            database_unknown_error(NameError.name)


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {'message': "User id '{}' not found."}, 404

        user.activated = True
        user.save_user()
        #return {'message': "User id '{}' confirmed successfully.".format(user_id)}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html', email=user.email, user=user.login), 200)
