from sql_alchemy import banco


class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, site_url):
        self.url = site_url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hotels': [hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, site_url):
        site = cls.query.filter_by(url=site_url).first()
        if site:
            return site
        return site

    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, site_url):
        self.url = site_url

    def delete_site(self):
        if self.hoteis:
            [banco.session.delete(hotel) for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()
