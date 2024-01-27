import pytesseract
import io

from bson import ObjectId

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from PIL import Image

MONGODB_URI = "mongodb+srv://Chyanna:chyannapassword@cluster92493.zrgv9ji.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGODB_URI)

app = Flask(__name__)
CORS(app)



@app.route('/assignments/', methods=['POST'])
def save_homework():
    data = request.json
    result = client['fyp']['assignment'].insert_one(data)  # Replace 'myCollection' with your collection
    print(data)
    return jsonify(str(result.inserted_id)), 201

@app.route('/teacher/<username>', methods=['GET'])
def get_classes_by_teacher(username):
    teacher = client['fyp']['teacher'].find_one({"username": username})
    if teacher:
        return jsonify(teacher['classes'])
    else:
        return jsonify([]), 404

# @app.route('/student/<class_name>', methods=['GET'])
# def get_students_by_class(class_name):
#     students = client['fyp']['student'].find({"class": class_name})
#     print(class_name)
#     print(students)
#     return jsonify([student for student in students])

# @app.route('/students/<class_name>', methods=['GET'])
# def get_student_names_by_class(class_name):
#     students_in_selected_class = client['fyp']['student'].find({"class": class_name})
#     studentList = {}
#     for student in students_in_selected_class:
#         studentList.update({student["name"]: student["number"]})
#     print(studentList)
#     return studentList

@app.route('/students/<class_name>', methods=['GET'])
def get_students_by_class(class_name):
    students_in_selected_class = client['fyp']['student'].find({'class': class_name})

    # Create a list of student dictionaries
    students_list = []
    for student in students_in_selected_class:
        # Construct a dictionary for each student
        student_data = {
            '_id': str(student['_id']),  # Convert ObjectId to string
            'name': student['name'],
            'number': student['number']
        }
        # Append the student dictionary to the list
        students_list.append(student_data)

    # Return the list of student dictionaries as JSON
    return jsonify(students_list)

# def save_text_to_db(student_id, text):
#     # Assuming 'student_id' is the string representation of the ObjectId
#     # If 'student_id' is not an ObjectId, you'll need to adjust the query accordingly
#     student_object_id = ObjectId(student_id)
#
#     # Update the student document with the OCR text
#     result = client['fyp']['submittedWork'].update_one(
#         {'_id': student_object_id},
#         {'$set': {'ocrText': text}}
#     )
#
#     # Check if the update was successful
#     if result.matched_count > 0:
#         print(f"Successfully uploaded assignment for student with id {student_id}")
#         return True
#     else:
#         print(f"No student found with id {student_id}")
#         return False
def save_text_to_db(student_id, text):
    # Create a new document with the student ID and OCR text
    new_document = {
        'studentId': ObjectId(student_id),  # Store the student ID as an ObjectId
        'ocrText': text,  # Store the extracted text
        # You can add more fields as necessary
    }

    # Insert the new document into the collection
    result = client['fyp']['submittedWork'].insert_one(new_document)

    # The insert_one method returns an InsertOneResult object
    if result.inserted_id:
        print(f"Successfully inserted new document with id {result.inserted_id}")
        return result.inserted_id  # You may want to return the new document ID
    else:
        print("Failed to insert new document.")
        return None
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

@app.route('/submittedWork', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Convert the file stream to an Image object
        image = Image.open(io.BytesIO(file.read()))
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image, lang='eng')

        # Here you would save 'text' to your database associated with the student
        student_id = request.form.get('student_id')
        save_text_to_db(student_id, text)

        return jsonify({'message': 'File processed', 'text': text})

    return jsonify({'error': 'Error processing file'}), 400



@app.route('/ping', methods=['GET'])
def ping():
    return jsonify("pong"), 200


if __name__ == '__main__':
    app.run(debug=True)

# for db_name in client.list_database_names():
#     print(db_name)
#     # client['fyp']["student.py"].insert_one({"name": "Chyanna", "age": 21})
#
# create_student(client, "mary", "23")
# student = get_student_by_name(client, "mary")
# print(student)
