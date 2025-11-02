from flask import request, jsonify
from config import app, db
from models import Server


@app.route("/servers", methods=["GET"])
def get_servers():
    servers = Server.query.all()
    json_servers = list(map(lambda x: x.to_json(), servers))
    return jsonify({"servers": json_servers})


@app.route("/create_server", methods=["POST"])
def create_server():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return (
            jsonify({"message": "You must include a first name, last name and email"}),
            400,
        )

    new_server = Server(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_server)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Server created!"}), 201


@app.route("/update_server/<int:server_id>", methods=["PATCH"])
def update_server(server_id):
    server = Server.query.get(server_id)

    if not server:
        return jsonify({"message": "Server not found"}), 404

    data = request.json
    server.first_name = data.get("firstName", server.first_name)
    server.last_name = data.get("lastName", server.last_name)
    server.email = data.get("email", server.email)

    db.session.commit()

    return jsonify({"message": "Server updated."}), 200


@app.route("/delete_server/<int:server_id>", methods=["DELETE"])
def delete_server(server_id):
    server = Server.query.get(server_id)

    if not server:
        return jsonify({"message": "Server not found"}), 404

    db.session.delete(server)
    db.session.commit()

    return jsonify({"message": "Server deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)