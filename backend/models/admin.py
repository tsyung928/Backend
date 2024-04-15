from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import secrets
from bson import ObjectId

def generate_password(length=12):
    # Generate a secure random password
    return secrets.token_hex(length)
def add_teacher(client):
    username = request.json.get('username')
    classes = request.json.get('classes')

    print (username)
    print (classes)

    if not username or not classes:
        return jsonify({"error": "Missing required fields"}), 400

    initial_password = generate_password()

    # Hash the initial password using werkzeug
    hashed_password = generate_password_hash(initial_password)

    # Splitting the classes string into a list, trimming whitespace
    classes_list = [class_name.strip() for class_name in classes.split(',')]

    # Inserting the teacher data into the MongoDB
    teacher_id = client['fyp']['teacher'].insert_one({
        "username": username,
        "classes": classes_list
    }).inserted_id

    client['fyp']['usersCollection'].insert_one({
        "username": username,
        "password": hashed_password,
        "role": "teacher"
    })

    return jsonify({"message": "Teacher added successfully", "teacher_id": str(teacher_id), "initial_password": initial_password}), 201

def delete_teacher(client, teacher_id):
    # Delete the teacher from the teacher collection
    username= client['fyp']['teacher'].find_one({'_id': ObjectId(teacher_id)})['username']
    print (username)
    client['fyp']['teacher'].find_one_and_delete({'_id': ObjectId(teacher_id)})

    # Delete the teacher from the users collection
    client['fyp']['usersCollection'].find_one_and_delete({'username': username})

    return jsonify({"message": "Teacher deleted successfully"}), 200

def update_teacher(client, teacher_id):
    # Get the updated data from the request
    updated_data = request.json
    print (updated_data)

    # Update the teacher data in the teacher collection
    client['fyp']['teacher'].update_one(
        {'_id': ObjectId(teacher_id)},
        {'$set': updated_data}
    )

    # Update the teacher data in the users collection
    client['fyp']['usersCollection'].update_one(
        {'username': updated_data['username']},
        {'$set': updated_data}
    )

    return jsonify({"message": "Teacher updated successfully"}), 200


def add_student (client):
    print (request.json)
    name = request.json.get('studentName')
    number = request.json.get('studentNumber')
    class_name = request.json.get('class')

    if not name or not number or not class_name:
        return jsonify({"error": "Missing required fields"}), 400

    # Inserting the student data into the MongoDB
    student_id = client['fyp']['student'].insert_one({
        "name": name,
        "number": number,
        "class": class_name
    }).inserted_id

    return jsonify({"message": "Student added successfully", "student_id": str(student_id)}), 201



def delete_student(client, student_id):
    # Delete the teacher from the teacher collection

    client['fyp']['student'].find_one_and_delete({'_id': ObjectId(student_id)})
    client['fyp']['submittedWork'].delete_many({'studentId': ObjectId(student_id)})

    return jsonify({"message": "Student deleted successfully"}), 200

def update_student(client, student_id):
    # Get the updated data from the request
    updated_data = request.json
    print(updated_data)

    # Remove the _id from the updated data if it exists
    updated_data.pop('_id', None)


    # Update the student data in the student collection
    client['fyp']['student'].update_one(
        {'_id': ObjectId(student_id)},
        {'$set': updated_data}
    )
    return jsonify({"message": "Student updated successfully"}), 200
