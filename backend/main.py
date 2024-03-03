import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from models.login import handle_login
from models.teacher import get_classes_by_teacher, to_get_teacher_list
from models.assignment import to_save_assignment, to_delete_assignment, to_update_assignment, \
    to_get_assignment_by_class, to_get_rubrics_by_assignment, \
    to_update_rubrics, to_create_assignment
from models.student import get_students_by_class, to_get_all_students_list
from models.ocr_google_vision import to_upload_and_process_pdf

MONGODB_URI = "mongodb+srv://Chyanna:chyannapassword@cluster92493.zrgv9ji.mongodb.net/"
client = MongoClient(MONGODB_URI)

bucket_name = 'fyp-bucket-tsy'
os.environ[
    'GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/chyanna/Desktop/FYP/MarkingApp/backend/venv/serious-bearing-412621-0ffe2185f86d.json'

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# reader = easyocr.Reader(['en'], gpu=False)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    return handle_login(username, password, client)  # Pass the users collection

@app.route('/assignments/', methods=['POST'])
def save_assignment():
    return to_save_assignment(client)

@app.route('/teachers/', methods=['GET'])
def get_teacher_list():
    return to_get_teacher_list(client)

@app.route('/teacher/<username>', methods=['GET'])
def classes_by_teacher(username):
    return get_classes_by_teacher(client, username)


@app.route('/students/', methods=['GET'])
def get_all_students_list():
    return to_get_all_students_list(client)

@app.route('/students/<class_name>', methods=['GET'])
def students_by_class(class_name):
    return get_students_by_class(client, class_name)

@app.route('/submittedWork', methods=['POST'])
def upload_and_process_pdf():
    return to_upload_and_process_pdf(client)

@app.route('/create_assignment', methods=['POST'])
def create_assignment():
    return to_create_assignment(client)

@app.route('/delete_assignment', methods=['POST'])
def delete_assignment():
    return to_delete_assignment(client)


@app.route('/update_assignment', methods=['POST'])
def update_assignment():
    return to_update_assignment(client)


@app.route('/assignment/<class_name>', methods=['GET'])
def get_assignment_by_class(class_name):
    return to_get_assignment_by_class(client, class_name)


@app.route('/assignment/assignment-title/<assignment_title>', methods=['GET'])
def get_rubrics_by_assignment(assignment_title):
    return to_get_rubrics_by_assignment(client, assignment_title)


@app.route('/assignment/update-rubrics', methods=['POST'])
def update_rubrics():
    return to_update_rubrics(client)


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify("pong"), 200


if __name__ == '__main__':
    app.run(debug=True)

