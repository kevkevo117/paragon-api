from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    character_class = db.Column(db.String(50), nullable=False)

    city = db.Column(db.String(100))