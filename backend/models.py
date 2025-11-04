from config import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
from datetime import timezone

class CredentialsHashModel(db.Model):
    """
    Abstract base model that provides username + password fields and helper methods.
    """

    __abstract__ = True

    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(CredentialsHashModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    servers = db.relationship('Server', backref='owner', lazy=True, cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
        }


class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_points = db.relationship('ServerData', backref='server', lazy=True, cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "ipAddress": self.ip_address,
            "userId": self.user_id,
        }


class ServerData(db.Model):
    __tablename__ = 'server_data'
    id = db.Column(db.Integer, primary_key=True)
    cpu_usage = db.Column(db.Float, nullable=False)
    memory_usage = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "cpuUsage": self.cpu_usage,
            "memoryUsage": self.memory_usage,
            "timestamp": self.timestamp.isoformat(),
            "serverId": self.server_id,
        }