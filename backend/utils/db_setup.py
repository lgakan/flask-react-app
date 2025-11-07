import random
from datetime import datetime, timedelta, timezone
from ..main import app, db
from ..models import User, Sensor, SensorData


def clear_and_seed_database():
    with app.app_context():
        print("Clearing the database...")
        db.drop_all()
        db.create_all()
        print("Database cleared and tables recreated.")

        print("Seeding Users...")
        users_to_create = [
            User(username="admin1", password="password", first_name="Admin", last_name="UserOne", email="admin1@example.com", is_admin=True),
            User(username="admin2", password="password", first_name="Admin", last_name="UserTwo", email="admin2@example.com", is_admin=True),
            User(username="user1", password="password", first_name="Normal", last_name="UserOne", email="user1@example.com", is_admin=False),
            User(username="user2", password="password", first_name="Normal", last_name="UserTwo", email="user2@example.com", is_admin=False),
        ]
        db.session.add_all(users_to_create)
        db.session.commit()
        print(f"Added {len(users_to_create)} users.")

        print("Seeding Sensors...")
        sensors_to_create = []
        for i in range(1, 11):
            sensor = Sensor(
                name=f"Server Room {i}",
                ip_address=f"192.168.1.{100 + i}"
            )
            sensors_to_create.append(sensor)

        db.session.add_all(sensors_to_create)
        db.session.commit()
        print(f"Added {len(sensors_to_create)} sensors.")

        print("Seeding Sensor Data...")
        all_sensors = Sensor.query.all()
        data_points_to_create = []
        total_data_points = 0

        for sensor in all_sensors:
            for i in range(10):
                timestamp = datetime.now(timezone.utc) - timedelta(hours=i)
                data_point = SensorData(
                    cpu_usage=round(random.uniform(1.0, 99.0), 2),
                    memory_usage=round(random.uniform(1.0, 99.0), 2),
                    timestamp=timestamp,
                    sensor_id=sensor.id
                )
                data_points_to_create.append(data_point)
                total_data_points += 1

        db.session.add_all(data_points_to_create)
        db.session.commit()
        print(f"Added {total_data_points} data points for {len(all_sensors)} sensors.")

        print("\nDatabase seeding complete!")


if __name__ == "__main__":
    clear_and_seed_database()