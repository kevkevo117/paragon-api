from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String(100), nullable=False)
    character_class = db.Column(db.String(100), nullable=False)

    city_id = db.Column(
        db.Integer,
        db.ForeignKey("city.id"),
        nullable=False
    )


class Kingdom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    cities = db.relationship(
        "City",
        backref="kingdom",
        lazy=True
    )


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    kingdom_id = db.Column(
        db.Integer,
        db.ForeignKey("kingdom.id"),
        nullable=False
    )

    characters = db.relationship(
        "Character",
        backref="city",
        lazy=True
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )