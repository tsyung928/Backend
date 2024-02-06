from flask import jsonify
from pymongo import MongoClient

def get_classes_by_teacher(client, username):
    teacher = client['fyp']['teacher'].find_one({"username": username})
    if teacher:
        return jsonify(teacher['classes'])
    else:
        return jsonify([]), 404

def to_get_teacher_list(client):
    teachers = list(
        client['fyp']['teacher'].find({}, {'_id': 0, 'username': 1, 'classes': 1}))  # Adjust projection as needed
    return jsonify(teachers)

