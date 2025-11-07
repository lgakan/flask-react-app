import random
from datetime import datetime
from ..main import app, db
from ..models import Sensor, SensorData


def generate_new_data_points():
    """
    Generates 1 new data point for each existing sensor in the database.
    This function is designed to be run on a schedule (e.g., a cron job).
    """
    with app.app_context():
        print(f"[{datetime.now()}] Starting data generation task...")
        sensors = Sensor.query.all()
        if not sensors:
            print("No sensors found in the database. Exiting.")
            return
        print(f"Found {len(sensors)} sensors. Generating new data points...")

        new_data_points = []
        for sensor in sensors:
            new_data = SensorData(
                sensor_id=sensor.id,
                cpu_usage=round(random.uniform(1.0, 99.0), 2),
                memory_usage=round(random.uniform(1.0, 99.0), 2),
            )
            new_data_points.append(new_data)
        db.session.add_all(new_data_points)
        db.session.commit()

        print(f"Successfully created {len(new_data_points)} new data points.")
        print(f"[{datetime.now()}] Data generation task finished.")


if __name__ == "__main__":
    generate_new_data_points()