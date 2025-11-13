import os
from config import app, db
from models import Sensor, User
from utils.db_setup import seed_database
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from datetime import timedelta
from routes.sensor_routes import sensor_bp
from routes.auth_routes import auth_bp

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default-super-secret-key-for-dev")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'Sensor API',
    'version': 3,
    "specs_route": "/api/docs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

# Initialize Flasgger
swagger = Swagger(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(sensor_bp)

if __name__ == "__main__":
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()

        # Check if the database is empty (by checking for sensors)
        if Sensor.query.count() == 0:
            print("Sensor table is empty. Seeding database with initial data...")
            seed_database()

    app.run(debug=True)