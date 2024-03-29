import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from models.login import handle_login
from models.marking import mark_and_save_marking, get_grades_by_assignment, to_update_grade
from models.profile import to_update_password
from models.teacher import get_classes_by_teacher, to_get_teacher_list
from models.assignment import to_save_assignment, to_delete_assignment, to_update_assignment, \
    to_get_assignment_by_class, to_get_rubrics_by_assignment, \
    to_update_rubrics, to_create_assignment, to_get_description_by_assignment, to_get_class_by_assignment, \
    to_get_title_by_assignment, to_get_homework_text_by_submissionId, to_get_type_by_assignment, to_get_types_by_teacher
from models.student import get_students_by_class, to_get_all_students_list
from models.ocr_google_vision import to_upload_and_process_pdf

MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)

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

@app.route('/assignment/fetch_types/<username>', methods=['GET'])
def get_types_by_teacher(username):
    return to_get_types_by_teacher(client, username)

@app.route('/assignment/fetch_type_by_title/<assignment_title>', methods=['GET'])
def get_type_by_assignment(assignment_title):
    return to_get_type_by_assignment(client, assignment_title)

@app.route('/assignment/fetch_rubrics_by_title/<assignment_title>', methods=['GET'])
def get_rubrics_by_assignment(assignment_title):
    return to_get_rubrics_by_assignment(client, assignment_title)

@app.route('/assignment/fetch_description_by_title/<assignment_title>', methods=['GET'])
def get_description_by_assignment(assignment_title):
    return to_get_description_by_assignment(client, assignment_title)


@app.route('/assignment/update-rubrics', methods=['POST'])
def update_rubrics():
    return to_update_rubrics(client)

@app.route('/start-marking', methods=['POST'])
def start_marking():
    return mark_and_save_marking(client)

@app.route('/marking/grades_after_mark/<assignmentId>', methods=['GET'])
def grades_after_marking(assignmentId):
    return get_grades_by_assignment(client, assignmentId)

@app.route('/assignment/get_class_by_assignmentid/<assignmentId>', methods=['GET'])
def get_class_by_assignment(assignmentId):
    return to_get_class_by_assignment(client, assignmentId)

@app.route('/assignment/get_title_by_assignmentid/<assignmentId>', methods=['GET'])
def get_title_by_assignment(assignmentId):
    return to_get_title_by_assignment(client, assignmentId)



@app.route('/marking/update_grade/<submissionId>', methods=['PUT'])
def update_grade(submissionId):
    return to_update_grade(client,submissionId)

@app.route('/assignment/get_homework_text_by_submissionId/<submissionId>', methods=['GET'])
def get_homework_text_by_submissionId(submissionId):
    return to_get_homework_text_by_submissionId(client, submissionId)

@app.route('/profile/update_password', methods=['PUT'])
def update_password():
    return to_update_password(client)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify("pong"), 200


if __name__ == '__main__':
    app.run(debug=True)

