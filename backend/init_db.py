from main import app
from models import db, Sensor
from utils.db_setup import seed_database


def initialize_database():
    """Creates database tables and seeds them if they are empty."""
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        if Sensor.query.count() == 0:
            print("Sensor table is empty. Seeding database with initial data...")
            seed_database()
            print("Database seeded successfully.")
        else:
            print("Database already contains data. Skipping seed.")
        print("Database initialization complete.")

if __name__ == "__main__":
    initialize_database()