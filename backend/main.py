from flask import request, jsonify
from config import app, db
from models import Sensor, SensorData
from utils.db_setup import seed_database


@app.route("/sensors", methods=["GET"])
def get_sensors():
    sensors = Sensor.query.all()
    json_sensors = list(map(lambda x: x.to_json(), sensors))
    return jsonify({"sensors": json_sensors})


@app.route("/create_sensor", methods=["POST"])
def create_sensor():
    name = request.json.get("name")
    ip_address = request.json.get("ipAddress")

    if not name or not ip_address:
        return (
            jsonify({"message": "You must include a sensor name and IP address"}),
            400,
        )

    new_sensor = Sensor(name=name, ip_address=ip_address)
    try:
        db.session.add(new_sensor)
        db.session.commit()
    except Exception as e:
        # This can happen if the IP address is not unique
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Sensor created!"}), 201


@app.route("/update_sensor/<int:sensor_id>", methods=["PATCH"])
def update_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    data = request.json
    sensor.name = data.get("name", sensor.name)
    sensor.ip_address = data.get("ipAddress", sensor.ip_address)

    db.session.commit()

    return jsonify({"message": "Sensor updated."}), 200


@app.route("/delete_sensor/<int:sensor_id>", methods=["DELETE"])
def delete_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    db.session.delete(sensor)
    db.session.commit()

    return jsonify({"message": "Sensor deleted!"}), 200


@app.route("/details_sensor/<int:sensor_id>", methods=["GET"])
def details_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    sensor_details = sensor.to_json()
    sensor_details["dataPoints"] = [data.to_json() for data in sensor.data_points]
    sensor_details["ownerName"] = f"{sensor.owner.first_name} {sensor.owner.last_name}"

    return jsonify(sensor_details), 200


@app.route("/sensor_data", methods=["POST"])
def create_sensor_data():
    sensor_id = request.json.get("sensorId")
    temperature = request.json.get("temperature")
    humidity = request.json.get("humidity")
    pressure = request.json.get("pressure")
    light_level = request.json.get("lightLevel")

    if (
            not sensor_id
            or temperature is None
            or humidity is None
            or pressure is None
            or light_level is None
    ):
        return jsonify({"message": "One of the required parameters is None."}), 400

    if not Sensor.query.get(sensor_id):
        return jsonify({"message": f"Sensor with id {sensor_id} not found."}), 404

    new_data_point = SensorData(
        sensor_id=sensor_id,
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        light_level=light_level
    )
    try:
        db.session.add(new_data_point)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify(new_data_point.to_json()), 201


@app.route("/sensor_data/<int:data_id>", methods=["PATCH"])
def update_sensor_data(data_id):
    data_point = SensorData.query.get_or_404(data_id, description="Data point not found")
    data = request.json

    data_point.temperature = data.get("temperature", data_point.temperature)
    data_point.humidity = data.get("humidity", data_point.humidity)
    data_point.pressure = data.get("pressure", data_point.pressure)
    data_point.light_level = data.get("lightLevel", data_point.light_level)

    db.session.commit()
    return jsonify({"message": "Data point updated."}), 200


@app.route("/sensor_data/<int:data_id>", methods=["DELETE"])
def delete_sensor_data(data_id):
    data_point = SensorData.query.get_or_404(data_id, description="Data point not found")
    db.session.delete(data_point)
    db.session.commit()
    return jsonify({"message": "Data point deleted."}), 200


if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Check if the database is empty (by checking for sensors)
        if Sensor.query.count() == 0:
            print("Sensor table is empty. Seeding database with initial data...")
            seed_database()

    app.run(debug=True)