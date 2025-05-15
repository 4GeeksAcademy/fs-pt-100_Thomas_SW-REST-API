from app import app, db
from models import Users, Favorites, People, Planets, Species, Vehicles, Pilots

with app.app_context():
    db.drop_all()
    db.create_all()

    #Users
    user1 = Users(email="thomas.mosley@example.com", password="1234", is_active=True)
    user2 = Users(email="thomas2.mosley2@example.com", password="1234", is_active=False)
    db.session.add_all([user1, user2])
    db.session.commit()

    #planets
    tatooine = Planets(
        name = "Tatooine",
        climate = "arid",
        surface_water = 1,
        diameter = 10465,
        gravity = "1 standard",
        orbital_period = 304,
        population = 200000,
    )
    alderaan = Planets(
        name = "Tatooine",
        climate = "temperate",
        surface_water = 40,
        diameter = 12500,
        gravity = "1 standard",
        orbital_period = 364,
        population = 2000000000,
    )
    db.session.add_all([tatooine, alderaan])
    db.session.commit()

    #species
    human = Species(
        name = "human",
        classification = "mammal",
        designation = "sentient",
        eye_colors = "brown, blue, green, hazel, grey, amber",
        skin_colors = "shades of peach and brown",
        language = "Galactic Basic",
        hair_colors = "blonde, brown, black, red",
        homeworld = tatooine,
        average_lifespan = 120,
        average_height = 180,
    )
    droid = Species(
        name = "droid",
        classification = "artificial",
        designation = "sentient",
        eye_colors = "n/a",
        skin_colors = "n/a",
        language = "n/a",
        hair_colors = "n/a",
        homeworld = tatooine,
        average_lifespan = None,
        average_height = "n/a",
    )
    db.session.add_all([human, droid])
    db.session.commit()

    #people
    luke = People(
        name = "Luke Skywalker",
        gender = "male",
        skin_color = "fair",
        hair_color = "blond",
        height = 172,
        eye_color = "blue",
        mass = 77,
        homeworld = tatooine,
        species = human
    )
    c3po = People(
        name = "C3PO",
        gender = "n/a",
        skin_color = "gold",
        hair_color = "n/a",
        height = 167,
        eye_color = "yellow",
        mass = 75,
        homeworld = tatooine,
        species = droid
    )
    leia = People(
        name = "Leia Organa",
        gender = "female",
        skin_color = "light",
        hair_color = "brown",
        height = 150,
        eye_color = "brown",
        mass = 49,
        homeworld = alderaan,
        species = human
    )
    db.session.add_all([luke, c3po, leia])
    db.session.commit()

    #residents and fauna
    tatooine.residents = [luke, c3po]
    tatooine.fauna = [human, droid]
    alderaan.residents = [leia]
    alderaan.fauna = [human]
    db.session.commit()

    #vehicles
    sand_crawler = Vehicles(
        name = "Sand Crawler",
        consumables = "2 months",
        cargo_capacity = 50000,
        max_atmosphering_speed = 30,
        crew = 46,
        length = 36.8,
        model = "Digger Crawler",
        vehicle_class = "wheeled",
    )
    landspeeder = Vehicles(
        name = "X-34 landspeeder",
        consumables = "unknown",
        cargo_capacity = 5,
        max_atmosphering_speed = 250,
        crew = 1,
        length = 3.4,
        model = "X-34 landspeeder",
        vehicle_class = "repulsorcraft",
    )
    db.session.add_all([sand_crawler, landspeeder])
    db.session.commit()

    #pilots
    pilot1 = Pilots(person=luke, vehicle=sand_crawler)
    pilot2 = Pilots(person=luke, vehicle=landspeeder)
    pilot3 = Pilots(person=c3po, vehicle=landspeeder)
    db.session.add_all([pilot1, pilot2, pilot3])
    db.session.commit()

    print("✅ Database seeded.")