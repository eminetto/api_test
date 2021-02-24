from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os, jwt
from datetime import datetime


app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True)
    # password = db.Column(db.String(100), unique=False)
    # image = db.Column(db.String(500), unique=False, nullable=True)


    def __init__(self, displayName, email):
        self.displayName = displayName
        self.email = email


# class Posts(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), unique=False)
#     content = db.Column(db.String(120), unique=True)
#     userId = db.Column('users',
#         db.Integer,
#         db.ForeignKey('users.id'),
#         nullable=False
#     )
#     users = db.relationship("Users", backref="post")
#     published = db.Column(db.Date, default=datetime.utcnow())
#     updated = db.Column(db.Date)
#
#
#     def __init__(self, title, userId):
#         self.title = username
#         self.userId = userId


@app.route("/")
def hello():
    return "Hello World!"

# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    data = request.get_json()

    if len(data['displayName'])<=8:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name field needs to be bigger than 8 characters'
        }), 400


    new_user = Users(
        displayName= data['displayName'],
        email = data['email']
    )

    db.session.add(new_user)
    db.session.commit()

    return {
        'id': new_user.id,
        'displayName': new_user.displayName,
        'email': new_user.email
    }, 201


#     """
#     Generates the Auth Token
#     :return: string
#     """
#     try:
#         payload = {
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
#             'iat': datetime.datetime.utcnow(),
#             'sub': user_id
#         }
#         return jwt.encode(
#             payload,
#             app.config.get('SECRET_KEY'),
#             algorithm='HS256'
#         )
#     except Exception as e:
#         return e


if __name__ == '__main__':
    app.run(debug=True)
