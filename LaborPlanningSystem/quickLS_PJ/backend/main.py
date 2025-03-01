from flask import Flask, jsonify, request
from backend.routes.associates import associates_bp
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Add this line


from backend.utils.database_setup import get_associates_collection, get_temp_changes_collection

associates_collection = get_associates_collection()
temp_changes_collection = get_temp_changes_collection()


# Register Blueprints (modular routing)
app.register_blueprint(associates_bp)

# Health check endpoint
@app.route("/")
def health_check():
    return {"status": "API is running!"}, 200

# Initialize JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure key
jwt = JWTManager(app)

# Mock user database (replace with your actual user database)
users = {
    "admin": {
        "username": "admin",
        "password": generate_password_hash("admin123"),  # Hashed password
        "role": "admin"
    },
    "manager": {
        "username": "manager",
        "password": generate_password_hash("manager123"),
        "role": "manager"
    }
}
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        access_token = create_access_token(identity=username)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "role": user['role']
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        "message": f"Hello, {current_user}!",
        "user": current_user
    }), 200

@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if users[current_user]['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(list(users.keys())), 200

@app.route('/api/users', methods=['POST'])
@jwt_required()
def add_user():
    current_user = get_jwt_identity()
    if users[current_user]['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = {
        "username": username,
        "password": generate_password_hash(password),
        "role": role
    }
    return jsonify({"message": "User added successfully"}), 201

@app.route('/api/users/<username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    current_user = get_jwt_identity()
    if users[current_user]['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    del users[username]
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)
