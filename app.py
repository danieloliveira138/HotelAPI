from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.user import User, UserRegister, UserLogin, UserLogout, UserConfirm
from resources.site import Site, Sites
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLOCKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    return jti in BLACKLIST


@jwt.revoked_token_loader
def invalidate_access_token(jwt_header, jwt_data):
    return jsonify({'message': 'You have been logged out'}), 401


api.add_resource(Hotels, '/hotel')
api.add_resource(Hotel, '/hotel/<string:hotel_id>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Sites, '/sites')
api.add_resource(Site, '/sites/<string:site_url>')
api.add_resource(UserConfirm, '/confirmation/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
