from flask import request, jsonify
from config import app, db
from models import User, Sensor, SensorData


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
    cpu_usage = request.json.get("cpuUsage")
    memory_usage = request.json.get("memoryUsage")

    if not sensor_id or cpu_usage is None or memory_usage is None:
        return jsonify({"message": "sensorId, cpuUsage, and memoryUsage are required."}), 400

    if not Sensor.query.get(sensor_id):
        return jsonify({"message": f"Sensor with id {sensor_id} not found."}), 404

    new_data_point = SensorData(sensor_id=sensor_id, cpu_usage=cpu_usage, memory_usage=memory_usage)
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

    data_point.cpu_usage = data.get("cpuUsage", data_point.cpu_usage)
    data_point.memory_usage = data.get("memoryUsage", data_point.memory_usage)

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
        db.create_all()

    app.run(debug=True)