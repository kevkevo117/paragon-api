from flask import Flask, jsonify, request
from models import Kingdom, db, Character, City

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paragon.db"

db.init_app(app)



@app.route("/")
def home():
    return {"message": "Welcome to the Paragon API"}

@app.route("/cities")
def get_cities():
    cities = City.query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "kingdom": c.kingdom.name
        }
        for c in cities
    ])

@app.route("/cities/<int:city_id>/characters")
def city_characters(city_id):

    city = City.query.get(city_id)

    if not city:
        return {"error": "City not found"}, 404

    return jsonify([
        {
            "id": char.id,
            "name": char.name,
            "race": char.race,
            "class": char.character_class
        }
        for char in city.characters
    ])

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
    city_id=data["city_id"]
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

@app.route("/kingdoms")
def get_kingdoms():

    kingdoms = Kingdom.query.all()

    return jsonify([
        {
            "id": k.id,
            "name": k.name,
            "cities": [c.name for c in k.cities]
        }
        for k in kingdoms
    ])


@app.route("/kingdoms/<int:kingdom_id>")
def get_kingdom(kingdom_id):

    kingdom = Kingdom.query.get(kingdom_id)

    if not kingdom:
        return {"error": "Kingdom not found"}, 404

    return {
        "id": kingdom.id,
        "name": kingdom.name,
        "cities": [c.name for c in kingdom.cities]
    }


with app.app_context():

    db.create_all()

    if Character.query.count() == 0:

        starter = Character(
            name="Aldric",
            race="Human",
            character_class="Paladin",
            city_id=1
        )

        db.session.add(starter)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)