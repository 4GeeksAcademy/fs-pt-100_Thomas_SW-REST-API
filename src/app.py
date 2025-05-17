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
    if not data or "email" not in data or "password" not in data or "is_active" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_user = Users(
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

@app.route("/users/<int:id>/favorites", methods=["GET"])
def get_favorites(id):
    stmt = select(Favorites).where(Users.id == id)
    favorites = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(favorites.serialize()), 200

@app.route("/favorite/planet/<int:id>", methods=["POST"])
def create_fav_planet():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_fav_planet = Favorites(
        name=data["name"]
    )
    db.session.add(new_fav_planet)
    db.session.commit()
    return jsonify(new_fav_planet.serialize()), 201

@app.route("/favorite/people/<int:id>", methods=["POST"])
def create_fav_person():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing data"}), 400
    new_fav_person = Users(
        name=data["name"]
    )
    db.session.add(new_fav_person)
    db.session.commit()
    return jsonify(new_fav_person.serialize()), 201

@app.route("/favorite/planet/<int:id>", methods=["DELETE"])
def delete_fav_planet(id):
    stmt = select(Favorites).where(Favorites.id == id)
    fav_planet = db.session.execute(stmt).scalar_one_or_none()
    if user is None:
        return jsonify({"error": "Planet not found"}), 404
    db.session.delete(fav_planet)
    db.session.commit()
    return jsonify({"message": "Planet deleted"}), 200

@app.route("/favorite/people/<int:id>", methods=["DELETE"])
def delete_fav_person(id):
    stmt = select(Favorites).where(Favorites.id == id)
    fav_person = db.session.execute(stmt).scalar_one_or_none()
    if fav_person is None:
        return jsonify({"error": "Person not found"}), 404
    db.session.delete(fav_person)
    db.session.commit()
    return jsonify({"message": "Person deleted"}), 200

##deprecated version
# @app.route('/people', methods=['GET'])
# def get_people():
#     people = People.query.all()
#     response_body = [obj.serialize() for obj in people]
#     return jsonify(response_body), 200

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
