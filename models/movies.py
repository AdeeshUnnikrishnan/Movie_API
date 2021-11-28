from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Asus\\Desktop\\api1\\movies_final.db'
db = SQLAlchemy(app) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    genre = db.Column(db.String(10))

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(50))
    genre = db.Column(db.String(10))
    review = db.Column(db.String(250))
    Up_vote = db.Column(db.Boolean)
    Down_vote = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
