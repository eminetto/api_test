from run import app, db
from models import Users
from flask import jsonify, request, make_response
import os, jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, re
from passlib.hash import pbkdf2_sha256 as sha256_crypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/user', methods =['GET'])
def get_user():


    users =  Users.query.all()

    return jsonify([
        {
            'id': user.id,
            'displayName': user.displayName,
            'email': user.email,
            'image': user.image
        }for user in users
    ])




@app.route("/user", methods=["POST"])
def add_user():
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    data = request.get_json()

    if 'displayName' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'displayName is required'
        }), 400

    if 'email' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'email is required'
        }), 400

    #validates email
    if not (re.search(regex,data['email'])):
        return jsonify({
            'error': 'Bad Request',
            'message': 'email must be a valid email'
        }), 400

    if len(data['displayName'])<8:
        return jsonify({
            'error': 'Bad Request',
            'message': 'displayName length must be at least 8 characters long'
        }), 400

    if len(data['password'])<6:
        return jsonify({
            'error': 'Bad Request',
            'message': 'password length must be at least 6 characters long'
        }), 400


    mail = Users.query.filter_by(email=data['email']).first()
    if mail:
        return jsonify({
            'message': 'Usuário já existe'
        }), 400
    else:
        new_user = Users(
            displayName= data['displayName'],
            email = data['email'],
            password = sha256_crypt.hash(data['password']),
            image = data['image']
        )

        db.session.add(new_user)
        db.session.commit()
        try:
            access_token = create_access_token(identity = new_user.displayName)
            refresh_token = create_refresh_token(identity = new_user.displayName)

            return jsonify({
                'access_token' : access_token,
                'refresh_token' : refresh_token
            })
        except:
            return jsonify({'message': 'Something went wrong'}), 500

@app.route("/login", methods=["POST"])
def login():
    # return auth()
    data = request.get_json()

    if 'password' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'password is required'
        }), 400

    if 'email' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'email is required'
        }), 400

    if len(data['password'])<1:
        return jsonify({
            'error': 'Bad Request',
            'message': 'password is not allowed to be empty'
        }), 400

    if len(data['email'])<1:
        return jsonify({
            'error': 'Bad Request',
            'message': 'email is not allowed to be empty'
        }), 400

    current_user = Users.query.filter_by(email=data['email']).first()

    if sha256_crypt.verify(data['password'], current_user.password):
        # return auth(mail, psw)
        access_token = create_access_token(identity = current_user.displayName)
        refresh_token = create_refresh_token(identity = current_user.displayName)
        return {
            'message': 'Logged in as {}'.format(current_user.displayName),
            'access_token': access_token,
            'refresh_token': refresh_token
            }
    else:
        return {'message': 'Wrong credentials'}

def token(user_id):
   token = jwt.encode({'public_id': user_id, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
   return token
