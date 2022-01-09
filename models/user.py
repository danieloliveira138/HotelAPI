from sql_alchemy import banco
from utils.constans import LOGIN_FIELD
from flask_jwt_extended import jwt_required


USERS = 'users'


class UserModel(banco.Model):
    __tablename__ = USERS

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    passwd = banco.Column(banco.String(40))

    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd

    def json(self):
        return {
            'user_id': self.user_id,
            LOGIN_FIELD: self.login
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
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
    def find_by_login(cls, login:str):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
