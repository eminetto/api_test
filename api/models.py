from run import db
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256 as sha256

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100), unique=False, nullable=False)
    image = db.Column(db.String(500), unique=False, nullable=True)


    def __init__(self, displayName, email, password, image):
        self.displayName = displayName
        self.email = email
        self.password = password
        self.image = image



class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    content = db.Column(db.String(120), unique=True)
    userId = db.Column('users',
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    users = db.relationship("Users", backref="post")
    published = db.Column(db.Date, default=datetime.utcnow())
    updated = db.Column(db.Date, default=datetime.utcnow())


    def __init__(self, title, content, userId):
        self.title = title
        self.content = content
        self.userId = userId
