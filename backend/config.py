from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
     r"/*": {
         "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"],
         "supports_credentials": True,
         "allow_headers": ["Content-Type", "Authorization"]
     }
 })

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)