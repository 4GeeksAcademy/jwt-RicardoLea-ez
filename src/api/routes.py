"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import timedelta

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Validar que se proporcionaron email y password
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400
        
        # Hashear la contraseña
        hashed_password = generate_password_hash(password).decode('utf-8')
        
        # Crear nuevo usuario
        new_user = User(
            email=email, 
            password=hashed_password, 
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "email": new_user.email
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error during registration: {str(e)}")
        return jsonify({"message": "Error during registration"}), 500

@api.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        # Validar que se proporcionaron email y password
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
        # Buscar usuario
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            # Crear token
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(hours=24)
            )
            
            return jsonify({
                "token": access_token,
                "user": {
                    "id": user.id,
                    "email": user.email
                },
                "message": "Login successful"
            }), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
            
    except Exception as e:
        print(f"Error during login: {str(e)}")
        return jsonify({"message": "Error during login"}), 500

@api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        return jsonify({
            "message": f"Hello {user.email}, you are accessing a protected endpoint!",
            "user": user.serialize()
        }), 200
        
    except Exception as e:
        return jsonify({"message": "Error accessing protected endpoint"}), 500

@api.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"valid": False}), 401
            
        return jsonify({
            "valid": True,
            "user": user.serialize()
        }), 200
        
    except Exception as e:
        return jsonify({"valid": False}), 401