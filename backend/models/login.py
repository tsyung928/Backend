from werkzeug.security import check_password_hash
from flask import jsonify

def handle_login(username, password, client):
    user = client['fyp']['usersCollection'].find_one({"username": username})
    role = user['role']
    if user and check_password_hash(user['password'], password):
        return jsonify({"role": role, "username": username, "message": "Login successful", "status": "success"}), 200
    else:
        return jsonify({"message": "Invalid credentials", "status": "fail"}), 401

