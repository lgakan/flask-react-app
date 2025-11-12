import os
from flask import request, jsonify
from config import app, db
from models import Sensor, SensorData, User
from utils.db_setup import seed_database
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, JWTManager
from datetime import timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default-super-secret-key-for-dev")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# --- Public Routes ---
@app.route("/sensors", methods=["GET"])
def get_sensors():
    sensors = Sensor.query.all()
    json_sensors = list(map(lambda x: x.to_json(), sensors))
    return jsonify({"sensors": json_sensors})


@app.route("/details_sensor/<int:sensor_id>", methods=["GET"])
def details_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    sensor_details = sensor.to_json()
    sensor_details["dataPoints"] = [data.to_json() for data in sensor.data_points]
    sensor_details["ownerName"] = f"{sensor.owner.first_name} {sensor.owner.last_name}"

    return jsonify(sensor_details), 200


# --- Authentication Routes ---
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')

    if not all([username, password, first_name, last_name, email]):
        return jsonify({"message": "All fields are required"}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "Username or email already exists"}), 400

    new_user = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(accessToken=access_token, refreshToken=refresh_token, user=user.to_json())

    return jsonify({"message": "Invalid username or password"}), 401


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(accessToken=new_access_token), 200


# --- Protected Routes ---
@app.route("/create_sensor", methods=["POST"])
@jwt_required(locations=["headers"])
def create_sensor():
    current_user_id = get_jwt_identity()
    name = request.json.get("name")
    ip_address = request.json.get("ipAddress")

    if not name or not ip_address:
        return jsonify({"message": "You must include a sensor name and IP address"}), 400

    new_sensor = Sensor(name=name, ip_address=ip_address, user_id=current_user_id)
    try:
        db.session.add(new_sensor)
        db.session.commit()
    except Exception as e:
        # This can happen if the IP address is not unique
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Sensor created!"}), 201


@app.route("/update_sensor/<int:sensor_id>", methods=["PATCH"])
@jwt_required(locations=["headers"])
def update_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    data = request.json
    sensor.name = data.get("name", sensor.name)
    sensor.ip_address = data.get("ipAddress", sensor.ip_address)

    db.session.commit()

    return jsonify({"message": "Sensor updated."}), 200


@app.route("/delete_sensor/<int:sensor_id>", methods=["DELETE"])
@jwt_required(locations=["headers"])
def delete_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    db.session.delete(sensor)
    db.session.commit()

    return jsonify({"message": "Sensor deleted!"}), 200


@app.route("/sensor_data", methods=["POST"])
@jwt_required(locations=["headers"])
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
@jwt_required(locations=["headers"])
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
@jwt_required(locations=["headers"])
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