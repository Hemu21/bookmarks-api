from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True,nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    book = db.relationship('bookmark',backref='User')
class bookmark(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String)
    short_url=db.Column(db.String)
    views=db.Column(db.Integer,default=0)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
