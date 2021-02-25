from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import string, random
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)


app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)
import views, models, resources

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()
