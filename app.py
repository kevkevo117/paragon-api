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
        "city": "Fortitudo",
        "character_class": "Paladin"
    },
    {
        "name": "Auryx",
        "race": "Dragon",
        "city": "Fortitudo",
        "character_class": "Sorcerer"
    },
    {
        "name": "Raviel",
        "race": "Goliath",
        "city": "Fortitudo",
        "character_class": "Barbarian"
    }
]

with app.app_context():

    if Character.query.count() == 0:

        starter = Character(
            name="Aldric",
            race="Human",
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

    characters = Character.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "class": c.character_class,
            "city": c.city,
            "race": c.race
        }
        for c in characters
    ])

@app.route("/characters/<int:character_id>", methods=["PUT"])
def update_character(character_id):

    character = Character.query.get(character_id)

    if not character:
        return {"error": "Character not found"}, 404

    data = request.get_json()

    character.name = data.get("name", character.name)
    character.race = data.get("race", character.race)
    character.character_class = data.get(
        "class",
        character.character_class
    )
    character.city = data.get("city", character.city)

    db.session.commit()

    return {
        "message": "Character updated",
        "character": {
            "id": character.id,
            "name": character.name,
            "race": character.race,
            "class": character.character_class,
            "city": character.city
        }
    }

@app.route("/characters/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):

    character = Character.query.get(character_id)

    if not character:
        return {"error": "Character not found"}, 404

    db.session.delete(character)
    db.session.commit()

    return {
        "message": f"Character {character.name} deleted"
    }

@app.route("/characters", methods=["POST"])
def create_character():

    data = request.get_json()

    required_fields = ["name", "race", "class", "city"]

    for field in required_fields:
        if field not in data:
            return {
                "error": f"Missing required field: {field}"
            }, 400

    character = Character(
        name=data["name"],
        race=data["race"],
        character_class=data["class"],
        city=data["city"]
    )

    db.session.add(character)
    db.session.commit()

    return {
        "id": character.id,
        "name": character.name,
        "class": character.character_class,
        "city": character.city,
        "race": character.race
    }, 201

@app.route("/cities/<city_name>")
def get_city(city_name):

    for city in cities:
        if city["name"].lower() == city_name.lower():
            return city

    return {"error": "City not found"}, 404

@app.route("/characters/<int:character_id>")
def get_character(character_id):

    character = Character.query.get(character_id)

    if not character:
        return {"error": "Character not found"}, 404

    return {
        "id": character.id,
        "name": character.name,
        "race": character.race,
        "class": character.character_class,
        "city": character.city
    }


with app.app_context():

    db.create_all()

    if Character.query.count() == 0:

        starter = Character(
            name="Aldric",
            race="Human",
            character_class="Paladin",
            city="Fortitudo"
        )

        db.session.add(starter)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)