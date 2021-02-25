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
@jwt_required
def get_users():


    users =  Users.query.all()

    return jsonify([
        {
            'id': user.id,
            'displayName': user.displayName,
            'email': user.email,
            'image': user.image
        }for user in users
    ])

@app.route('/user/<id>/', methods =['GET'])
@jwt_required
def get_user(id):

    user =  Users.query.filter_by(id=id).first_or_404()

    return jsonify(
        {
            'id': user.id,
            'displayName': user.displayName,
            'email': user.email,
            'image': user.image
        }
    )

@app.route('/user/<id>/', methods =['DELETE'])
@jwt_required
def delete_user(id):

    user =  Users.query.filter_by(id=id).first_or_404()

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message' : 'user deleted successfully',
    })


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
            access_token = create_access_token(identity = new_user.id)
            refresh_token = create_refresh_token(identity = new_user.id)

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
        access_token = create_access_token(identity = current_user.id)
        refresh_token = create_refresh_token(identity = current_user.id)
        return {
            'message': 'Logged in as {}'.format(current_user.displayName),
            'access_token': access_token,
            'refresh_token': refresh_token
            }
    else:
        return {'message': 'Wrong credentials'}

@app.route("/post", methods=["POST"])
@jwt_required
def add_post():
    # regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    data = request.get_json()
    #
    if 'title' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'title is required'
        }), 400

    if 'content' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'content is required'
        }), 400

    post = Posts.query.filter_by(title=data['title']).first()
    if post:
        return jsonify({
            'message': 'Usuário já existe'
        }), 400
    else:
        try:
            new_post = Posts(
                title= data['title'],
                content = data['content'],
                userId = Users.query.filter_by(id=get_jwt_identity()).first()
            )

            db.session.add(new_post)
            db.session.commit()

        except:
            return jsonify({'message': 'Something went wrong'}), 500

@app.route('/post', methods =['GET'])
@jwt_required
def get_posts():

    posts = Posts.query.all()
    user = Users.query.filter_by(id=post.userId).first()

    return jsonify([
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'published': post.published,
            'updated': post.updated,
            'user':{
                [
                    'id': post.userId,
                    {
                    'displayName' : user.displayName,
                    'email': user.email,
                    'image': user.image
                    }

                ]
            }
        }for post in posts
    ])

@app.route('/post/<id>/', methods =['GET'])
@jwt_required
def get_post(id):

    post =  Posts.query.filter_by(id=id).first_or_404()

    return jsonify([
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'published': post.published,
            'updated': post.updated,
            'user':{
                [
                    'id': post.userId,
                    {
                    'displayName' : post.users.displayName,
                    'email': post.users.email,
                    'image': post.users.image
                    }

                ]
            }
        }
    ])

@app.route('/post/<id>/', methods =['PUT'])
@jwt_required
def edit_post(id):
    data = request.get_json()

    if 'title' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'title is required'
        }), 400

    if 'content' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'content is required'
        }), 400

    post =  Posts.query.filter_by(id=id).first_or_404()
    try:
        post.title= data['title'],
        post.content = data['content'],
        post.userId = Users.query.filter_by(id=get_jwt_identity()).first()
        db.session.commit()

        return jsonify([
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'published': post.published,
                'updated': post.updated,
                'user':{
                    [
                        'id': post.userId,
                        {
                        'displayName' : post.users.displayName,
                        'email': post.users.email,
                        'image': post.users.image
                        }

                    ]
                }
            }
        ]), 201
    except:
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/post/search/', methods =['GET'])
@jwt_required
def search_post(id):
    return

def token(user_id):
   token = jwt.encode({'public_id': user_id, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
   return token
