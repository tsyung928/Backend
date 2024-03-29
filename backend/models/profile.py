from flask import request, jsonify
from werkzeug.security import generate_password_hash


def to_update_password(client):
    data = request.get_json()
    # It's a good practice to hash passwords before storing
    hashed_password = generate_password_hash(data['newPassword'])

    # Find the user by their username and update their password
    result = client['fyp']['usersCollection'].update_one(
        {'username': data['username']},
        {'$set': {'password': hashed_password}}
    )

    if result.modified_count:
        return jsonify({'success': True, 'message': 'Password updated successfully'}), 200
    else:
        # No document found with the provided username or the password is the same
        return jsonify({'success': False, 'message': 'Password update failed'}), 404
