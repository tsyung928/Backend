from flask import jsonify
from pymongo import MongoClient

def get_classes_by_teacher(client, username):
    teacher = client['fyp']['teacher'].find_one({"username": username})
    if teacher:
        return jsonify(teacher['classes'])
    else:
        return jsonify([]), 404