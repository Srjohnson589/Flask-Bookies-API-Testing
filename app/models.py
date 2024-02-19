from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

user_already_read = db.Table(
    'user_already_read',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('book_id', db.String, db.ForeignKey('book.book_id'))
)

user_want_to_read = db.Table(
    'user_current_book',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'))
)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    current_book = db.Column(db.String, db.ForeignKey('book.book_id'))
    already_read = db.relationship('Book',
                             secondary=user_already_read,
                             backref="read_by",
                             lazy="dynamic")
    want_to_read = db.relationship('Book',
                             secondary=user_want_to_read,
                             backref="wanted_by",
                             lazy="dynamic")
    
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    img_small = db.Column(db.String, nullable=True)
    img_large = db.Column(db.String, nullable=True)
    author = db.Column(db.String, db.ForeignKey(''))

    def __init__(self, name, hp, attack, defense, sprite_img):

    def save(self):
        db.session.add(self)
        db.session.commit()

class Author(db.Model):
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))

    def __init__(self, name, hp, attack, defense, sprite_img):

    def save(self):
        db.session.add(self)
        db.session.commit()