from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
from models.site import SiteModel
from utils.message_helper import help_message_field_blank, database_unknown_error


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url', type=str, required=True, help=help_message_field_blank("url"))

    @jwt_required()
    def get(self, site_url):
        try:
            site = SiteModel.find_site(site_url)
            if site:
                return site.json(), 200
            return {'message': 'Site not found'}, 404
        except:
            return database_unknown_error()

    @jwt_required()
    def post(self, site_url):
        try:
            if SiteModel.find_site(site_url):
                return {"message": "Hotel id \'{}\' already exists.".format(site_url)}, 400
            site = SiteModel(site_url)
            site.save_site()
            return site.json(), 200
        except:
            return database_unknown_error()

    @jwt_required()
    def put(self, site_url):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str, required=True, help=help_message_field_blank('url'))
        data = parser.parse_args()
        try:
            saved_site = SiteModel.find_site(site_url)
            if saved_site:
                saved_site.update_site(*data)
                saved_site.save_site()
                return saved_site.json(), 200
            site = SiteModel(site_url)
            return site.json(), 200
        except:
            database_unknown_error()

    @jwt_required()
    def delete(self, site_url):
        try:
            site = SiteModel.find_site(site_url)
            if site:
                site.delete_site()
                return {'message': 'hotel deleted'}, 200
            return {'message': 'Site not founded.'}, 404
        except NameError:
            return database_unknown_error(NameError.name)
