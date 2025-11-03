"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import request, jsonify, Blueprint
from api.models import db, User
from api.utils import APIException
from flask_cors import CORS
import traceback
import bcrypt
import jwt
from datetime import datetime, timedelta

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
        print("=== SIGNUP INICIADO ===")
        data = request.get_json()
        print("Datos recibidos:", data)
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400
        
        # Hashear la contraseña con bcrypt (MANERA CORREGIDA)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Crear nuevo usuario
        new_user = User(
            email=email, 
            password=hashed_password.decode('utf-8'),  # Decodificar antes de guardar
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        print("✅ Usuario registrado exitosamente:", email)
        
        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "email": new_user.email
            }
        }), 201
        
    except Exception as e:
        print("❌ ERROR en signup:", str(e))
        print("🔍 Traceback:", traceback.format_exc())
        db.session.rollback()
        return jsonify({"message": "Error during registration"}), 500

@api.route('/login', methods=['POST'])
def login():
    try:
        print("=== LOGIN INICIADO ===")
        data = request.get_json()
        print("Datos recibidos:", data)
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
        # Buscar usuario
        user = User.query.filter_by(email=email).first()
        print("Usuario encontrado:", user.email if user else "No encontrado")
        
        if user:
            # Verificar contraseña (MANERA CORREGIDA)
            # Primero codificar la contraseña ingresada
            password_bytes = password.encode('utf-8')
            
            # Si el password guardado es bytes, usarlo directamente, sino codificarlo
            if isinstance(user.password, bytes):
                stored_password = user.password
            else:
                stored_password = user.password.encode('utf-8')
            
            print("🔐 Verificando contraseña...")
            if bcrypt.checkpw(password_bytes, stored_password):
                print("✅ Contraseña correcta")
                
                # Crear token JWT simple
                token_payload = {
                    'user_id': user.id,
                    'email': user.email,
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }
                
                # Usar una clave secreta
                token = jwt.encode(token_payload, 'secret-key-change-in-production', algorithm='HS256')
                
                return jsonify({
                    "token": token,
                    "user": {
                        "id": user.id,
                        "email": user.email
                    },
                    "message": "Login successful"
                }), 200
            else:
                print("❌ Contraseña incorrecta")
                return jsonify({"message": "Invalid credentials"}), 401
        else:
            print("❌ Usuario no encontrado")
            return jsonify({"message": "Invalid credentials"}), 401
            
    except Exception as e:
        print("❌ ERROR en login:", str(e))
        print("🔍 Traceback:", traceback.format_exc())
        return jsonify({"message": "Error during login"}), 500

@api.route('/test-db', methods=['GET'])
def test_db():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_data = user.serialize()
            user_data['password_type'] = type(user.password).__name__
            user_list.append(user_data)
            
        return jsonify({
            "message": "Database connection successful",
            "users_count": len(users),
            "users": user_list
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/reset-users', methods=['POST'])
def reset_users():
    """Eliminar todos los usuarios existentes para empezar limpio"""
    try:
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Deleted {len(users)} users"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500