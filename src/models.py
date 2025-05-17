from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }
    
class Favorites(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(nullable=False)
    item_type: Mapped[str] = mapped_column(nullable=False)
    item_name: Mapped[str] = mapped_column(String(120))

    user: Mapped["Users"] = relationship(back_populates="favorites")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_type": self.item_type,
            "item_id": self.item_id,
            "item_name": self.item_name
        }
    
class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(120))
    skin_color: Mapped[str] = mapped_column(String(120))
    hair_color: Mapped[str] = mapped_column(String(120))
    height: Mapped[int] = mapped_column(Integer())
    eye_color: Mapped[str] = mapped_column(String(120))
    mass: Mapped[int] = mapped_column(Integer())

    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=True)
    species: Mapped["Species"] = relationship(back_populates="members")

    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    homeworld: Mapped["Planets"] = relationship(back_populates="residents")

    def serialize(self):
        from models import db, Favorites
        favorites = db.session.query(Favorites).filter_by(
            item_type="person",
            item_id=self.id
        ).all()
        favorited_by = [fav.user.name for fav in favorites if fav.user]

        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "eye_color": self.eye_color,
            "mass": self.mass,
            "species": self.species.name if self.species else None,
            "homeworld": self.homeworld.name if self.homeworld else None,
            "favorited_by": favorited_by
        }

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate:  Mapped[str] = mapped_column(String(120))
    surface_water: Mapped[int] = mapped_column(Integer())
    diameter: Mapped[int] = mapped_column(Integer())
    gravity: Mapped[str] = mapped_column(String(120))
    orbital_period: Mapped[int] = mapped_column(Integer())
    population: Mapped[int] = mapped_column(Integer())
    
    residents: Mapped[list["People"]] = relationship(back_populates="homeworld")
    fauna: Mapped[list["Species"]] = relationship(back_populates="homeworld")

    def serialize(self):
        from models import db, Favorites
        favorites = db.session.query(Favorites).filter_by(
            item_type="planet",
            item_id=self.id
        ).all()
        favorited_by = [fav.user.name for fav in favorites if fav.user]
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "surface_water": self.surface_water,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "residents": [resident.name for resident in self.residents] if self.residents else None,
            "fauna": [species.name for species in self.fauna] if self.fauna else None,
            "favorited_by": favorited_by
        }

class Species(db.Model):
    __tablename__ = "species"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    classification: Mapped[str] = mapped_column(String(120))
    designation: Mapped[str] = mapped_column(String(120))
    eye_colors: Mapped[str] = mapped_column(String(120))
    skin_colors: Mapped[str] = mapped_column(String(120))
    language: Mapped[str] = mapped_column(String(120))
    hair_colors: Mapped[str] = mapped_column(String(120))
    average_lifespan:  Mapped[int] = mapped_column(Integer(), nullable=True)
    average_height:  Mapped[int] = mapped_column(Integer(), nullable=True)
    
    homeworld_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=True)
    homeworld: Mapped["Planets"] = relationship(back_populates="fauna")

    members: Mapped[list["People"]] = relationship(back_populates="species")

    def serialize(self):
        from models import db, Favorites
        favorites = db.session.query(Favorites).filter_by(
            item_type="species",
            item_id=self.id
        ).all()
        favorited_by = [fav.user.name for fav in favorites if fav.user]
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "eye_colors": self.eye_colors,
            "skin_colors": self.skin_colors,
            "language": self.language,
            "hair_colors": self.hair_colors,
            "average_lifespan": self.average_lifespan,
            "average_height": self.average_height,
            "homeworld": self.homeworld.name if self.homeworld else None,
            "members": [member.name for member in self.members] if self.members else None,
            "favorited_by": favorited_by
        }

class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(120))
    consumables: Mapped[str] = mapped_column(String(120))
    cargo_capacity: Mapped[int] = mapped_column(Integer())
    max_atmosphering_speed: Mapped[int] = mapped_column(Integer())
    crew: Mapped[int] = mapped_column(Integer())
    length: Mapped[int] = mapped_column(Integer())
    model: Mapped[str] = mapped_column(String(120))
    vehicle_class: Mapped[str] = mapped_column(String(120))

    def serialize(self):
        from models import db, Favorites
        favorites = db.session.query(Favorites).filter_by(
            item_type="vehicle",
            item_id=self.id
        ).all()
        favorited_by = [fav.user.name for fav in favorites if fav.user]
        return {
            "id": self.id,
            "name": self.name,
            "consumables": self.consumables,
            "cargo_capacity": self.cargo_capacity,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "crew": self.crew,
            "length": self.length,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "favorited_by": favorited_by
        }

