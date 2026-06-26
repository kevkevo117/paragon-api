from flask import Flask, jsonify, request
from models import Kingdom, db, Character, City, User
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paragon.db"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in production

db.init_app(app)
jwt = JWTManager(app)


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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    required_fields = ["username", "password"]

    for field in required_fields:
        if field not in data:
            return {
                "error": f"Missing required field: {field}"
            }, 400

    if User.query.filter_by(username=data["username"]).first():
        return {
            "error": "Username already exists"
        }, 409

    hashed_password = generate_password_hash(data["password"])

    user = User(
        username=data["username"],
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return {
        "message": "User registered successfully"
    }, 201


with app.app_context():

    db.create_all()

    kingdom = Kingdom.query.first()

    if kingdom is None:
        kingdom = Kingdom(name="Paragon")
        db.session.add(kingdom)
        db.session.commit()

    city = City.query.first()

    if city is None:
        city = City(
            name="Fortitudo",
            kingdom_id=kingdom.id
        )
        db.session.add(city)
        db.session.commit()

    if Character.query.count() == 0:
        starter = Character(
            name="Aldric",
            race="Human",
            character_class="Paladin",
            city_id=city.id
        )

        db.session.add(starter)
        db.session.commit()
if __name__ == "__main__":
    app.run(debug=True)