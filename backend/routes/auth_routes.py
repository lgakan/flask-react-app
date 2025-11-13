from flask import Blueprint, request, jsonify
from ..models import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
            - firstName
            - lastName
            - email
          properties:
            username:
              type: string
            password:
              type: string
            firstName:
              type: string
            lastName:
              type: string
            email:
              type: string
          example:
            username: "newuser"
            password: "strongpassword123"
            firstName: "John"
            lastName: "Doe"
            email: "john.doe@example.com"
    responses:
      201: {description: 'User created successfully'}
      400: {description: 'Invalid input or user already exists'}
    """
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


@auth_bp.route('/login', methods=['POST'])
def login():
    """Logs in a user and returns access and refresh tokens
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [username, password]
          properties:
            username:
              type: string
              example: 'testuser'
            password:
              type: string
              example: 'password'
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            accessToken: {type: string}
            refreshToken: {type: string}
            user: {type: object}
        examples:
          application/json:
            accessToken: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNjQyNjgzMiwianRpIjoiYjU4YjM..."
            refreshToken: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNjQyNjgzMiwianRpIjoiYjU4YjM..."
            user:
              id: 1
              username: "testuser"
              email: "admin1@example.com"
              firstName: "Admin"
              lastName: "UserOne"
      401: {description: 'Invalid username or password'}
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(accessToken=access_token, refreshToken=refresh_token, user=user.to_json())

    return jsonify({"message": "Invalid username or password"}), 401


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=str(current_user_id))
    return jsonify(accessToken=new_access_token), 200


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """Get the profile of the currently logged-in user
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: User profile data
        schema:
          type: object
        examples:
          application/json:
            email: "admin1@example.com"
            firstName: "Admin"
            id: 1
            lastName: "UserOne"
            username: "admin1"
          # You can define the full user schema here if desired
      404: {description: 'User not found'}
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_json()), 200


@auth_bp.route('/change_password', methods=['PATCH'])
@jwt_required()
def change_password():
    """Change the current user's password
    ---
    tags:
      - User
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [currentPassword, newPassword]
          properties:
            currentPassword:
              type: string
              description: The user's current password.
            newPassword:
              type: string
              description: The desired new password.
          example:
            currentPassword: "old_secure_password"
            newPassword: "new_very_secure_password"
    responses:
      200: {description: 'Password updated successfully'}
      400: {description: 'Missing password fields'}
      401: {description: 'Invalid current password'}
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    data = request.get_json()
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    if not current_password or not new_password:
        return jsonify({"message": "Current password and new password are required"}), 400
    if not user.check_password(current_password):
        return jsonify({"message": "Invalid current password"}), 401
    user.password = new_password
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200