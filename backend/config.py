import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Get allowed origins from environment variable, split by comma, with a fallback for development
allowed_origins_str = os.environ.get("CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',')]

CORS(app, resources={
     r"/*": {
         "origins": allowed_origins,
         "supports_credentials": True,
         "allow_headers": ["Content-Type", "Authorization"]
     }
 })

# Use environment variable for the database URI, with a default for local SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///mydatabase.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)