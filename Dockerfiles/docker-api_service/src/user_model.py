import json
from flask_sqlalchemy import SQLAlchemy
from settings import app

# This is written in the format
# sqlite:///(ABSOLUTE PATH)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'username': self.name, 'password': self.price}

    def add_user(_username, _password):
        new_user = User(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()

    def get_user(_username, _password):
        user = User.query.filter_by(username=_username).filter_by(password=_password).first()
        if user is None:
            return False
        else:
            return True

    def get_all_users():
        return User.query.all()

    def __repr__(self):
        user_object = {
            'username': self.username,
            'password': self.password
        }
        return json.dumps(user_object)