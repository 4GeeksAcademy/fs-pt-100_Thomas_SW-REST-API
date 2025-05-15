from app import app, db
from models import Users, Favorites, People, Planets, Species, Vehicles

with app.app_context():
    db.drop_all()
    db.create_all()

    #Users
    user1 = Users(email="thomas.mosley@example.com", password="1234", is_active=True)
    user2 = Users(email="thomas2.mosley2@example.com", password="1234", is_active=False)
    db.session.add_all([user1, user2])
    db.session.commit()

    print("✅ Data seeded.")