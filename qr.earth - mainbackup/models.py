from flask import current_app
from itsdangerous import Serializer
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        print(f"Serializer created with SECRET_KEY: {current_app.config['SECRET_KEY']} and expires_sec: {expires_sec}")
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        print(f"Generated token: {token}")
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)