"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Favorites, People, Planets, Species, Vehicles
from sqlalchemy import select

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = db.session.execute(select(Users)).scalars().all()
    return jsonify([obj.serialize() for obj in users]), 200

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data  or "name" not in data or "email" not in data or "password" not in data or "is_active" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_user = Users(
        name=data["name"],
        email=data["email"],
        password=data["password"],
        is_active=data["is_active"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    user.email = data.get("email", user.email) 
    user.password = data.get("password", user.password)
    user.is_active = data.get("is_active", user.is_active)
    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    stmt = select(Users).where(Users.id == id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

@app.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    current_user_id = 1 #to update later with authentication
    stmt = select(Favorites).where(Users.id == current_user_id)
    favorites = db.session.execute(stmt).scalars().all()
    if favorites is None:
        return jsonify({"error": "Favorites not found"}), 404
    return jsonify([fav.serialize() for fav in favorites]), 200

@app.route("/favorite/people/<int:id>", methods=["POST"])
def create_fav_person(id):
    current_user_id = 1 #to update later with authentication
    user = db.session.get(Users, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    person = db.session.get(People, id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    existing_fav = db.session.execute(
        db.select(Favorites).where(
            Favorites.user_id == current_user_id,
            Favorites.item_id == people.id,
            Favorites.item_type == "people"
        )
    ).scalars().first()
    if existing_fav:
        return jsonify({"error": "Person already in favorites"}), 400
    new_fav_person = Favorites(
        user_id=current_user_id,
        item_id=person.id,
        item_type="person",
        item_name=person.name
    )
    db.session.add(new_fav_person)
    db.session.commit()
    return jsonify(new_fav_person.serialize()), 201

@app.route("/favorite/planet/<int:id>", methods=["POST"])
def create_fav_planet(id):
    current_user_id = 1 #to update later with authentication
    user = db.session.get(Users, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    planet = db.session.get(Planets, id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    existing_fav = db.session.execute(
        db.select(Favorites).where(
            Favorites.user_id == current_user_id,
            Favorites.item_id == planet.id,
            Favorites.item_type == "planet"
        )
    ).scalars().first()
    if existing_fav:
        return jsonify({"error": "Planet already in favorites"}), 400
    new_fav_planet = Favorites(
        user_id=current_user_id,
        item_id=planet.id,
        item_type="planet",
        item_name=planet.name
    )
    db.session.add(new_fav_planet)
    db.session.commit()
    return jsonify(new_fav_planet.serialize()), 201

@app.route("/favorite/species/<int:id>", methods=["POST"])
def create_fav_species(id):
    current_user_id = 1 #to update later with authentication
    user = db.session.get(Users, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    species = db.session.get(Species, id)
    if not species:
        return jsonify({"error": "Species not found"}), 404
    existing_fav = db.session.execute(
        db.select(Favorites).where(
            Favorites.user_id == current_user_id,
            Favorites.item_id == species.id,
            Favorites.item_type == "species"
        )
    ).scalars().first()
    if existing_fav:
        return jsonify({"error": "Species already in favorites"}), 400
    new_fav_species = Favorites(
        user_id=current_user_id,
        item_id=species.id,
        item_type="species",
        item_name=species.name
    )
    db.session.add(new_fav_species)
    db.session.commit()
    return jsonify(new_fav_species.serialize()), 201

@app.route("/favorite/vehicle/<int:id>", methods=["POST"])
def create_fav_vehicle(id):
    current_user_id = 1 #to update later with authentication
    user = db.session.get(Users, current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    vehicle = db.session.get(Vehicles, id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    existing_fav = db.session.execute(
        db.select(Favorites).where(
            Favorites.user_id == current_user_id,
            Favorites.item_id == vehicle.id,
            Favorites.item_type == "vehicle"
        )
    ).scalars().first()
    if existing_fav:
        return jsonify({"error": "Vehicle already in favorites"}), 400
    new_fav_vehicle = Favorites(
        user_id=current_user_id,
        item_id=vehicle.id,
        item_type="vehicle",
        item_name=vehicle.name
    )
    db.session.add(new_fav_vehicle)
    db.session.commit()
    return jsonify(new_fav_vehicle.serialize()), 201

@app.route("/people", methods=["POST"])
def create_person():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_person = People(
        name=data["name"],
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

@app.route("/planets", methods=["POST"])
def create_planet():
    data = request.get_json()
    if not data  or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_planet = Planets(
        name=data["name"],
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route("/species", methods=["POST"])
def create_species():
    data = request.get_json()
    if not data  or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_species = Species(
        name=data["name"],
    )
    db.session.add(new_species)
    db.session.commit()
    return jsonify(new_species.serialize()), 201

@app.route("/vehicles", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    if not data  or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_vehicle = Vehicles(
        name=data["name"],
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201

@app.route("/people/<int:id>", methods=["PUT"])
def update_person(id):
    data = request.get_json()
    stmt = select(People).where(People.id == id)
    person = db.session.execute(stmt).scalar_one_or_none()
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    person.eye_color = data.get("eye_color", person.eye_color) 
    person.gender = data.get("gender", person.gender)
    person.hair_color = data.get("hair_color", person.hair_color)
    person.height = data.get("height", person.height)
    person.mass = data.get("mass", person.mass)
    person.name = data.get("name", person.name)
    person.skin_color = data.get("skin_color", person.skin_color)

    species_id = data.get("species_id")
    if species_id is not None:
        species = db.session.get(Species, species_id)
        if not species:
            return jsonify({"error": "Invalid species_id"}), 400
        person.species = species

    homeworld_id = data.get("homeworld_id")
    if homeworld_id is not None:
        homeworld = db.session.get(Planets, homeworld_id)
        if not homeworld:
            return jsonify({"error": "Invalid homeworld_id"}), 400
        person.homeworld = homeworld

    db.session.commit()
    return jsonify(person.serialize()), 200

@app.route("/planets/<int:id>", methods=["PUT"])
def update_planet(id):
    data = request.get_json()
    stmt = select(Planets).where(Planets.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    planet.climate = data.get("climate", planet.climate) 
    planet.diameter = data.get("diameter", planet.diameter)
    planet.gravity = data.get("gravity", planet.gravity)
    planet.name = data.get("name", planet.name)
    planet.orbital_period = data.get("orbital_period", planet.orbital_period)
    planet.population = data.get("population", planet.population)
    planet.surface_water = data.get("surface_water", planet.surface_water)

    fauna_ids = data.get("fauna_ids")
    if fauna_ids is not None:
        species_list = db.session.query(Species).filter(Species.id.in_(fauna_ids)).all()
        if len(species_list) != len(fauna_ids):
            return jsonify({"error": "One or more fauna species not found"}), 400
        planet.fauna = species_list

    residents_ids = data.get("residents_ids")
    if residents_ids is not None:
        people =  db.session.query(People).filter(People.id.in_(residents_ids)).all()
        if len(people) != len(residents_ids):
            return jsonify({"error": "One or more residents not found"}), 400
        planet.residents = people

    db.session.commit()
    return jsonify(planet.serialize()), 200

@app.route("/species/<int:id>", methods=["PUT"])
def update_species(id):
    data = request.get_json()
    stmt = select(Species).where(Species.id == id)
    species = db.session.execute(stmt).scalar_one_or_none()
    if species is None:
        return jsonify({"error": "Species not found"}), 404
    species.average_height = data.get("average_height", species.average_height) 
    species.average_lifespan = data.get("average_lifespan", species.average_lifespan)
    species.classification = data.get("classification", species.classification)
    species.designation = data.get("designation", species.designation)
    species.eye_colors = data.get("eye_colors", species.eye_colors)
    species.hair_colors = data.get("hair_colors", species.hair_colors)
    species.language = data.get("language", species.language)
    species.name = data.get("name", species.name)
    species.skin_colors = data.get("skin_colors", species.skin_colors)

    homeworld_id = data.get("homeworld_id")
    if homeworld_id is not None:
        homeworld = db.session.get(Planets, homeworld_id)
        if not homeworld:
            return jsonify({"error": "Invalid homeworld_id"}), 400
        species.homeworld = homeworld

    members_ids = data.get("members_ids")
    if members_ids is not None:
        people =  db.session.query(People).filter(People.id.in_(members_ids)).all()
        if len(people) != len(residents_ids):
            return jsonify({"error": "One or more members not found"}), 400
        species.members = people

    db.session.commit()
    return jsonify(species.serialize()), 200

@app.route("/vehicles/<int:id>", methods=["PUT"])
def update_vehicle(id):
    data = request.get_json()
    stmt = select(Vehicles).where(Vehicles.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    vehicle.cargo_capacity = data.get("cargo_capacity", vehicle.cargo_capacity) 
    vehicle.consumables = data.get("consumables", vehicle.consumables)
    vehicle.crew = data.get("crew", vehicle.crew)
    vehicle.length = data.get("length", vehicle.length)
    vehicle.max_atmosphering_speed = data.get("max_atmosphering_speed", vehicle.max_atmosphering_speed)
    vehicle.model = data.get("model", vehicle.model)
    vehicle.name = data.get("name", vehicle.name)
    vehicle.vehicle_class = data.get("vehicle_class", vehicle.vehicle_class)
    db.session.commit()
    return jsonify(vehicle.serialize()), 200

@app.route("/favorites/<int:id>", methods=["DELETE"])
def delete_fav(id):
    current_user_id = 1 #to update later with authentication
    stmt = select(Favorites).where(
        Favorites.user_id == current_user_id,
        Favorites.id == id
        )
    fav = db.session.execute(stmt).scalar_one_or_none()
    if fav is None:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 200

@app.route("/favorite/people/<int:id>", methods=["DELETE"])
def delete_fav_person(id):
    current_user_id = 1 #to update later with authentication
    stmt = select(Favorites).where(
        Favorites.user_id == current_user_id,
        Favorites.item_type == "person",
        Favorites.item_id == id
        )
    fav_person = db.session.execute(stmt).scalar_one_or_none()
    if fav_person is None:
        return jsonify({"error": "Favorite person not found"}), 404
    db.session.delete(fav_person)
    db.session.commit()
    return jsonify({"message": "Favorite person deleted"}), 200

@app.route("/favorite/planet/<int:id>", methods=["DELETE"])
def delete_fav_planet(id):
    current_user_id = 1 #to update later with authentication
    stmt = select(Favorites).where(
        Favorites.user_id == current_user_id,
        Favorites.item_type == "planet",
        Favorites.item_id == id
        )
    fav_planet = db.session.execute(stmt).scalar_one_or_none()
    if fav_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404
    db.session.delete(fav_planet)
    db.session.commit()
    return jsonify({"message": "Favorite planet deleted"}), 200

@app.route("/favorite/species/<int:id>", methods=["DELETE"])
def delete_fav_species(id):
    current_user_id = 1 #to update later with authentication
    stmt = select(Favorites).where(
        Favorites.user_id == current_user_id,
        Favorites.item_type == "species",
        Favorites.item_id == id
        )
    fav_species = db.session.execute(stmt).scalar_one_or_none()
    if fav_species is None:
        return jsonify({"error": "Favorite species not found"}), 404
    db.session.delete(fav_species)
    db.session.commit()
    return jsonify({"message": "Favorite species deleted"}), 200

@app.route("/favorite/vehicle/<int:id>", methods=["DELETE"])
def delete_fav_vehicle(id):
    current_user_id = 1 #to update later with authentication
    stmt = select(Favorites).where(
        Favorites.user_id == current_user_id,
        Favorites.item_type == "vehicle",
        Favorites.item_id == id
        )
    fav_vehicle = db.session.execute(stmt).scalar_one_or_none()
    if fav_vehicle is None:
        return jsonify({"error": "Favorite vehicle not found"}), 404
    db.session.delete(fav_vehicle)
    db.session.commit()
    return jsonify({"message": "Favorite vehicle deleted"}), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = db.session.execute(select(People)).scalars().all()
    return jsonify([obj.serialize() for obj in people]), 200

@app.route("/people/<int:id>", methods=["GET"])
def get_person(id):
    stmt = select(People).where(People.id == id)
    person = db.session.execute(stmt).scalar_one_or_none()
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = db.session.execute(select(Planets)).scalars().all()
    return jsonify([obj.serialize() for obj in planets]), 200

@app.route("/planets/<int:id>", methods=["GET"])
def get_planet(id):
    stmt = select(Planets).where(Planets.id == id)
    planet = db.session.execute(stmt).scalar_one_or_none()
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/species', methods=['GET'])
def get_all_species():
    species = db.session.execute(select(Species)).scalars().all()
    return jsonify([obj.serialize() for obj in species]), 200

@app.route("/species/<int:id>", methods=["GET"])
def get_species(id):
    stmt = select(Species).where(Species.id == id)
    species = db.session.execute(stmt).scalar_one_or_none()
    if species is None:
        return jsonify({"error": "Species not found"}), 404
    return jsonify(species.serialize()), 200

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = db.session.execute(select(Vehicles)).scalars().all()
    return jsonify([obj.serialize() for obj in vehicles]), 200

@app.route("/vehicles/<int:id>", methods=["GET"])
def get_vehicle(id):
    stmt = select(Vehicles).where(Vehicles.id == id)
    vehicle = db.session.execute(stmt).scalar_one_or_none()
    if vehicle is None:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
