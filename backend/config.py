import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Get allowed origins from environment variable, with a fallback for local development
CORS_ORIGINS = "https://flask-react-app-frontend.onrender.com"

CORS(app, resources={
     r"/*": {
         "origins": CORS_ORIGINS,
         "supports_credentials": True,
         "allow_headers": ["Content-Type", "Authorization"]
     }
 })

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)