from flask import Flask, jsonify, request
from models import db, Character

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paragon.db"

db.init_app(app)

cities = [
    {"name": "Fortitudo", "region": "Paragon"},
    {"name": "Unitatem", "region": "Paragon"},
    {"name": "Simultas", "region": "Paragon"},
    {"name": "Aeternitas", "region": "Paragon"}
]

characters = [
    {
        "name": "Solomon",
        "race": "Aasimar",
        "city": "Fortitudo"
    },
    {
        "name": "Auryx",
        "race": "Dragon",
        "city": "Fortitudo"
    },
    {
        "name": "Raviel",
        "race": "Goliath",
        "city": "Fortitudo"
    }
]

with app.app_context():

    if Character.query.count() == 0:

        starter = Character(
            name="Aldric",
            character_class="Paladin",
            city="Fortitudo"
        )

        db.session.add(starter)
        db.session.commit()

    db.create_all()

@app.route("/")
def home():
    return {"message": "Welcome to the Paragon API"}

@app.route("/cities")
def get_cities():
    return jsonify(cities)

@app.route("/characters")
def get_characters():
    return jsonify(characters)

@app.route("/characters", methods=["POST"])
def create_character():

    new_character = request.json

    new_character["id"] = len(characters) + 1

    characters.append(new_character)

    return new_character, 201

@app.route("/cities/<city_name>")
def get_city(city_name):

    for city in cities:
        if city["name"].lower() == city_name.lower():
            return city

    return {"error": "City not found"}, 404

@app.route("/characters/<character_name>")
def get_character(character_name):

    for character in characters:
        if character["name"].lower() == character_name.lower():
            return character

    return {"error": "Character not found"}, 404

@app.route("/dbcharacters")
def get_db_characters():

    characters = Character.query.all()

    results = []

    for character in characters:
        results.append({
            "id": character.id,
            "name": character.name,
            "class": character.character_class,
            "city": character.city
        })

    return jsonify(results)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)