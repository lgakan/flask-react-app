from flask import Blueprint, request, jsonify
from models import Sensor, SensorData, db
from flask_jwt_extended import jwt_required, get_jwt_identity

sensor_bp = Blueprint('sensor_bp', __name__)


# --- Public Sensor Routes ---
@sensor_bp.route("/sensors", methods=["GET"])
def get_sensors():
    """Get a list of all sensors
    This is a public endpoint.
    ---
    tags:
      - Sensors
    responses:
      200:
        description: A list of sensors
        schema:
          type: object
          properties:
            sensors: {type: array, items: {type: object}}
        examples:
          application/json:
            sensors:
              - id: 1
                name: "Living Room Temp"
                ip_address: "192.168.1.101"
                user_id: 1
              - id: 2
                name: "Garage Humidity"
                ip_address: "192.168.1.102"
                user_id: 2
    """
    sensors = Sensor.query.all()
    json_sensors = list(map(lambda x: x.to_json(), sensors))
    return jsonify({"sensors": json_sensors})


@sensor_bp.route("/details_sensor/<int:sensor_id>", methods=["GET"])
def details_sensor(sensor_id):
    """Get detailed information for a single sensor, including its data points
    This is a public endpoint.
    ---
    tags:
      - Sensors
    parameters:
      - name: sensor_id
        in: path
        type: integer
        required: true
        description: The ID of the sensor to retrieve.
    responses:
      200:
        description: Detailed information about the sensor.
        schema:
          type: object
        examples:
          application/json:
            id: 1
            name: "Living Room Temp"
            ip_address: "192.168.1.101"
            user_id: 1
            ownerName: "Admin UserOne"
            dataPoints:
              - id: 101
                sensor_id: 1
                temperature: 22.5
                humidity: 45.2
                pressure: 1012.5
                lightLevel: 550.0
                timestamp: "2025-11-13T10:30:00"
      404: {description: 'Sensor not found'}
    """
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    sensor_details = sensor.to_json()
    # Order data points by timestamp for consistency
    data_points = sorted(sensor.data_points, key=lambda dp: dp.timestamp)
    sensor_details["dataPoints"] = [data.to_json() for data in data_points]
    sensor_details["ownerName"] = f"{sensor.owner.first_name} {sensor.owner.last_name}"
    return jsonify(sensor_details), 200


# --- Protected Sensor Routes ---
@sensor_bp.route("/create_sensor", methods=["POST"])
@jwt_required(locations=["headers"])
def create_sensor():
    """Create a new sensor
    This endpoint creates a new sensor and associates it with the logged-in user.
    ---
    tags:
      - Sensors
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [name, ipAddress]
          properties:
            name:
              type: string
              description: The name of the sensor.
              example: "Living Room Temp"
            ipAddress:
              type: string
              description: The IP address of the sensor.
              example: "192.168.1.101"
    responses:
      201: {description: 'Sensor created successfully'}
      400: {description: 'Invalid input data'}
    """
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
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "Sensor created!"}), 201


@sensor_bp.route("/update_sensor/<int:sensor_id>", methods=["PATCH"])
@jwt_required(locations=["headers"])
def update_sensor(sensor_id):
    """Update an existing sensor
    ---
    tags:
      - Sensors
    security:
      - Bearer: []
    parameters:
      - name: sensor_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The new name of the sensor.
            ipAddress:
              type: string
              description: The new IP address of the sensor.
          example:
            name: "Updated Living Room Sensor"
            ipAddress: "192.168.1.254"
    responses:
      200: {description: 'Sensor updated successfully'}
      404: {description: 'Sensor not found'}
    """
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    data = request.json
    sensor.name = data.get("name", sensor.name)
    sensor.ip_address = data.get("ipAddress", sensor.ip_address)
    db.session.commit()
    return jsonify({"message": "Sensor updated."}), 200


@sensor_bp.route("/delete_sensor/<int:sensor_id>", methods=["DELETE"])
@jwt_required(locations=["headers"])
def delete_sensor(sensor_id):
    """Delete a sensor
    ---
    tags:
      - Sensors
    security:
      - Bearer: []
    parameters:
      - name: sensor_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: 'Sensor deleted successfully'}
      404: {description: 'Sensor not found'}
    """
    sensor = Sensor.query.get_or_404(sensor_id, description="Sensor not found")
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({"message": "Sensor deleted!"}), 200


# --- Protected Sensor Data Routes ---
@sensor_bp.route("/sensor_data", methods=["POST"])
@jwt_required(locations=["headers"])
def create_sensor_data():
    """Create a new data point for a sensor
    ---
    tags:
      - Sensor Data
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [sensorId, temperature, humidity]
          properties:
            sensorId:
              type: integer
            temperature:
              type: number
              format: float
            humidity:
              type: number
              format: float
            pressure:
              type: number
              format: float
            lightLevel:
              type: number
              format: float
            timestamp:
              type: string
              format: date-time
          example:
            sensorId: 1
            temperature: 21.5
            humidity: 48.9
            pressure: 1013.1
            lightLevel: 600
            timestamp: "2025-11-13T12:00:00Z"
    responses:
      201: {description: 'Data point created successfully'}
      400: {description: 'Invalid or missing data'}
      404: {description: 'Sensor not found'}
    """
    data = request.json
    sensor_id = data.get("sensorId")
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    pressure = data.get("pressure")
    light_level = data.get("lightLevel")

    if not all(k in data and data[k] is not None for k in ["sensorId", "temperature", "humidity"]):
        return jsonify({"message": "sensorId, temperature, and humidity are required."}), 400

    if not Sensor.query.get(sensor_id):
        return jsonify({"message": f"Sensor with id {sensor_id} not found."}), 404

    new_data_point = SensorData(
        sensor_id=sensor_id,
        temperature=temperature,
        humidity=humidity,
        pressure=pressure,
        light_level=light_level
    )
    db.session.add(new_data_point)
    db.session.commit()
    return jsonify(new_data_point.to_json()), 201


@sensor_bp.route("/sensor_data/<int:data_id>", methods=["GET"])
@jwt_required(locations=["headers"])
def get_sensor_data(data_id):
    """Get a single sensor data point by its ID
    ---
    tags:
      - Sensor Data
    security:
      - Bearer: []
    parameters:
      - name: data_id
        in: path
        type: integer
        required: true
        description: The ID of the sensor data point to retrieve.
    responses:
      200:
        description: A single sensor data point.
        schema:
          type: object
        examples:
          application/json:
            id: 101
            sensor_id: 1
            temperature: 22.5
            humidity: 45.2
            pressure: 1012.5
            lightLevel: 550.0
            timestamp: "2025-11-13T10:30:00"
          # You can define the full SensorData schema here if you want more detail
      401: {description: 'Missing or invalid token'}
      404: {description: 'Data point not found'}
    """
    data_point = SensorData.query.get_or_404(data_id, description="Data point not found")
    return jsonify(data_point.to_json()), 200


@sensor_bp.route("/sensor_data/<int:data_id>", methods=["PATCH"])
@jwt_required(locations=["headers"])
def update_sensor_data(data_id):
    """Update an existing sensor data point
    ---
    tags:
      - Sensor Data
    security:
      - Bearer: []
    parameters:
      - name: data_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            temperature:
              type: number
              format: float
            humidity:
              type: number
              format: float
            pressure:
              type: number
              format: float
            lightLevel:
              type: number
              format: float
          example:
            temperature: 22.1
            humidity: 47.5
    responses:
      200: {description: 'Data point updated successfully'}
      404: {description: 'Data point not found'}
    """
    data_point = SensorData.query.get_or_404(data_id, description="Data point not found")
    data = request.json
    data_point.temperature = data.get("temperature", data_point.temperature)
    data_point.humidity = data.get("humidity", data_point.humidity)
    data_point.pressure = data.get("pressure", data_point.pressure)
    data_point.light_level = data.get("lightLevel", data_point.light_level)
    db.session.commit()
    return jsonify({"message": "Data point updated."}), 200


@sensor_bp.route("/sensor_data/<int:data_id>", methods=["DELETE"])
@jwt_required(locations=["headers"])
def delete_sensor_data(data_id):
    """Delete a sensor data point
    ---
    tags:
      - Sensor Data
    security:
      - Bearer: []
    parameters:
      - name: data_id
        in: path
        type: integer
        required: true
    responses:
      200: {description: 'Data point deleted successfully'}
      404: {description: 'Data point not found'}
    """
    data_point = SensorData.query.get_or_404(data_id, description="Data point not found")
    db.session.delete(data_point)
    db.session.commit()
    return jsonify({"message": "Data point deleted."}), 200