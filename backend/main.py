from flask import request, jsonify
from config import app, db
from models import User, Server, ServerData


@app.route("/servers", methods=["GET"])
def get_servers():
    servers = Server.query.all()
    json_servers = list(map(lambda x: x.to_json(), servers))
    return jsonify({"servers": json_servers})


@app.route("/create_server", methods=["POST"])
def create_server():
    name = request.json.get("name")
    ip_address = request.json.get("ipAddress")
    # user_id = request.json.get("userId")
    user_id = 1 # TODO: CHANGE ME LATER

    if not name or not ip_address or not user_id:
        return (
            jsonify({"message": "You must include a server name, IP address, and userId"}),
            400,
        )

    # Check if the user exists
    if not User.query.get(user_id):
        return jsonify({"message": f"User with id {user_id} not found."}), 404

    new_server = Server(name=name, ip_address=ip_address, user_id=user_id)
    try:
        db.session.add(new_server)
        db.session.commit()
    except Exception as e:
        # This can happen if the IP address is not unique
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Server created!"}), 201


@app.route("/update_server/<int:server_id>", methods=["PATCH"])
def update_server(server_id):
    server = Server.query.get_or_404(server_id, description="Server not found")
    data = request.json
    server.name = data.get("name", server.name)
    server.ip_address = data.get("ipAddress", server.ip_address)

    db.session.commit()

    return jsonify({"message": "Server updated."}), 200


@app.route("/delete_server/<int:server_id>", methods=["DELETE"])
def delete_server(server_id):
    server = Server.query.get_or_404(server_id, description="Server not found")
    db.session.delete(server)
    db.session.commit()

    return jsonify({"message": "Server deleted!"}), 200


@app.route("/details_server/<int:server_id>", methods=["GET"])
def details_server(server_id):
    server = Server.query.get_or_404(server_id, description="Server not found")
    server_details = server.to_json()
    server_details["dataPoints"] = [data.to_json() for data in server.data_points]
    server_details["ownerName"] = f"{server.owner.first_name} {server.owner.last_name}"

    return jsonify(server_details), 200


@app.route("/server_data", methods=["POST"])
def create_server_data():
    server_id = request.json.get("serverId")
    cpu_usage = request.json.get("cpuUsage")
    memory_usage = request.json.get("memoryUsage")

    if not server_id or cpu_usage is None or memory_usage is None:
        return jsonify({"message": "serverId, cpuUsage, and memoryUsage are required."}), 400

    if not Server.query.get(server_id):
        return jsonify({"message": f"Server with id {server_id} not found."}), 404

    new_data_point = ServerData(server_id=server_id, cpu_usage=cpu_usage, memory_usage=memory_usage)
    try:
        db.session.add(new_data_point)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify(new_data_point.to_json()), 201


@app.route("/server_data/<int:data_id>", methods=["PATCH"])
def update_server_data(data_id):
    data_point = ServerData.query.get_or_404(data_id, description="Data point not found")
    data = request.json

    data_point.cpu_usage = data.get("cpuUsage", data_point.cpu_usage)
    data_point.memory_usage = data.get("memoryUsage", data_point.memory_usage)

    db.session.commit()
    return jsonify({"message": "Data point updated."}), 200


@app.route("/server_data/<int:data_id>", methods=["DELETE"])
def delete_server_data(data_id):
    data_point = ServerData.query.get_or_404(data_id, description="Data point not found")
    db.session.delete(data_point)
    db.session.commit()
    return jsonify({"message": "Data point deleted."}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)