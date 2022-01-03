from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel

app = Flask(__name__)
api = Api(app)

api.add_resource(Hotels, '/hotel')
api.add_resource(Hotel, '/hotel/<string:hotel_id>')

if __name__ == '__main__':
    app.run(debug=True)