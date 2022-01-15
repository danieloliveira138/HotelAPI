from sql_alchemy import banco
from utils.constans import LOGIN_FIELD
from flask_jwt_extended import jwt_required
from flask import request, url_for
from requests import post


USERS = 'users'
MAILGUN_DOMAIN = 'sandboxac99cc97d20d40ac8bb02c018559022a.mailgun.org'
MAILGUN_API_KEY = 'fbe479b62cafecdd3f0340ded3f17657-76f111c4-f0be4abc'
FROM_TITLE = 'NO-REPLY'
FROM_MAIL = 'no-reply@restapi.com'


class UserModel(banco.Model):
    __tablename__ = USERS

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    passwd = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    activated = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, passwd, email, activated):
        self.login = login
        self.passwd = passwd
        self.email = email
        self.activated = activated

    def json(self):
        return {
            'user_id': self.user_id,
            LOGIN_FIELD: self.login,
            'activated': self.activated
        }

    def send_confirmation_email(self):
        link = request.root_url[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post(
            'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
            auth=('api', MAILGUN_API_KEY),
            data={
                'from': '{} <{}>'.format(FROM_TITLE, FROM_MAIL),
                'to': self.email,
                'subject': 'Confirmação de Cadastro',
                'text': 'Confirme seu cadastro clicando no link a seguir: {}'.format(link),
                'html': '<html><p>\
                        Confirme seu cadastro clicando no link a seguir: <a href="{}">CONFIRMAR EMAIL</a>\
                        </p></html>'.format(link)
                }
            )

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    @jwt_required()
    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()

    @classmethod
    def find_by_login(cls, login: str):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
