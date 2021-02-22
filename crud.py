from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, validate
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100), unique=False, nullable=False)
    image = db.Column(db.String(500), unique=False)


    def __init__(self, username, email):
        self.displayName = username
        self.email = email

    # @validates('email')
    # def validate_email(self, key, address):
    #     assert '@' in address
    #     return address

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('displayName', 'email')


user_schema = UsersSchema()
users_schema = UserSchema(many=True)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    content = db.Column(db.String(120), unique=True)
    userId = db.Column(db.Integer, ForeignKey('users.id'))
    users = relationship("Users")
    published = db.Column(db.Date, default=datetime.utcnow())
    updated = db.Column(db.Date)


    def __init__(self, username, email):
        self.title = username
        self.userId = email

# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    displayName = request.json['displayName']
    email = request.json['email']
    if len(data['displayName'])<=8:
        return {
            'error': 'Bad Request',
            'message': 'Name field needs to be bigger than 8 characters'
        }, 400

    new_user = Users(displayName, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)

# @app.route("/login", methods=["GET"])
# def get_user():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
#     return jsonify(result.data)

def get_token_auth_header():


    return token

if __name__ == '__main__':
    app.run(debug=True)
