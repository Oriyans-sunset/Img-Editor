from enum import unique
from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///UsersDB.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    img = db.Column(db.BLOB)
    mimetype = db.Column(db.Text)
    filename = db.Column(db.String)

with app.app_context():
    db.create_all()
