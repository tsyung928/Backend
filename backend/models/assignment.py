from bson import ObjectId
from flask import jsonify, request
from pymongo import MongoClient



def to_save_assignment(client):
    data = request.json
    result = client['fyp']['assignment'].insert_one(data)  # Replace 'myCollection' with your collection
    return jsonify(str(result.inserted_id)), 201

def save_text_to_db(client, student_id, assignment_id, text):
    # Create a new document with the student ID and OCR text
    new_document = {
        'studentId': ObjectId(student_id),  # Store the student ID as an ObjectId
        'assignmentId': ObjectId(assignment_id),  # Store the assignment ID as an ObjectId
        'ocrText': text,  # Store the extracted text
        # You can add more fields as necessary
    }
    query = {'studentId': student_id, 'assignmentId': assignment_id}

    existing_entry = get_submitted_work_by_studentid_and_assignmentid(client, student_id, assignment_id)
    #existing_entry=client['fyp']['submittedWork'].find_one({'studentId': student_id, 'assignmentId': assignment_id})

    if existing_entry:
        # If it exists, update the text
        result = client['fyp']['submittedWork'].update_one(
            query,
            {'$set': {'ocrText': text}}
        )
        if result.modified_count == 0:
            print("No documents were updated. Something went wrong.")
        else:
            print(f"Updated document with student_id: {student_id}, assignment_id: {assignment_id}")
    else:
        # If it doesn't exist, create a new entry
        result = client['fyp']['submittedWork'].insert_one({
            'studentId': student_id,
            'assignmentId': assignment_id,
            'ocrText': text
        })
        if result.inserted_id:
            print(f"Inserted new document with student_id: {student_id}, assignment_id: {assignment_id}")
        else:
            print("No new document was inserted. Something went wrong.")

def to_create_assignment(client):
    # Get the data from the request
    data = request.get_json()

    # Insert the homework data into the database
    result = client['fyp']['assignment'].insert_one(data)

    if result.inserted_id:
        return jsonify({'message': 'Homework created successfully', 'id': str(result.inserted_id)})
    else:
        return jsonify({'error': 'Failed to create homework'}), 500

def to_delete_assignment(client):
    data = request.get_json()
    class_name = data.get('class')
    assignment_title = data.get('assignment_title')
    assignment= client['fyp']['assignment'].find_one({'class': class_name, 'title': assignment_title})

    # Delete the assignment details
    client['fyp']['assignment'].delete_one({'class': class_name, 'title': assignment_title})

    # Delete the uploaded documents associated with this assignment
    client['fyp']['submittedWork'].delete_many({'assignmentId': str(assignment['_id'])})

    return jsonify({'message': 'Assignment and related documents deleted successfully'}), 200

def to_update_assignment(client):
    data = request.get_json()
    result = client['fyp']['assignment'].update_one(
        {'class': data['class'], 'title': data['title']},
        {
            '$set': {
                'rubrics': data['rubrics'],
                'description': data['description']
            }
        }
    )
    assignmentId = client['fyp']['assignment'].find_one({'class':data['class'], 'title':data['title']})
    if result.modified_count:
        return jsonify({'success': True, 'id': str(assignmentId['_id'])}), 200
    else:
        return jsonify({'success': False, 'id': str(assignmentId['_id'])}), 404

def to_get_assignment_by_class(client, class_name):
    assignments = client['fyp']['assignment'].find({"class": class_name}, {"_id": 0, "title": 1})
    assignment_titles  = [assignment['title'] for assignment in assignments]
    return jsonify(assignment_titles)

def to_get_rubrics_by_assignment(client, assignment_title):
    # Find the homework by title and return its rubrics
    # Assuming each homework title is unique
    assignment = client['fyp']['assignment'].find_one({"title": assignment_title})
    if assignment:
        return jsonify({
            'rubrics': assignment['rubrics']
        })
    else:
        return jsonify('No assignment found'), 404

def to_get_description_by_assignment(client, assignment_title):
    # Assuming each homework title is unique
    assignment = client['fyp']['assignment'].find_one({"title": assignment_title})
    if assignment:
        return jsonify({
            'description': assignment['description']
        })
    else:
        return jsonify('No assignment found'), 404

def to_get_types_by_teacher(client, teacher_username):
    teacher = client['fyp']['teacher'].find_one({"username": teacher_username})
    classes = teacher['classes']
    print(classes)
    types = []

    for class_name in classes:
        print(class_name)
        assignments = client['fyp']['assignment'].find({"class": class_name})

        for assignment in assignments:
            # Check if 'type' key exists and if the value is not already in the list
            if 'type' in assignment:
                for type in assignment['type']:
                    if type not in types:
                        print(type)
                        types.append(type)

    print(types)
    return jsonify(types)



def to_get_type_by_assignment(client, assignment_title):
    assignment = client['fyp']['assignment'].find_one({"title": assignment_title})

    if assignment:
        print(assignment['type'])
        return jsonify({
            'type': assignment['type']
        })
    else:
        return jsonify('No assignment found'), 404


def to_get_types_by_class(client, classname):
    assignments = client['fyp']['assignment'].find({"class": classname})
    types = []

    for assignment in assignments:
        if 'type' in assignment:
            for type in assignment['type']:
                if type not in types:
                    types.append(type)

    return jsonify(types)

def to_get_title_by_id(client, assignment_id):
    assignment = client['fyp']['assignment'].find_one({"_id": ObjectId(assignment_id)})
    if assignment:
        return jsonify({
            'title': assignment['title']
        })
    else:
        return jsonify('No assignment found'), 404
def to_update_rubrics(client):
    data = request.get_json()
    class_name = data.get('class')
    homework_title = data.get('homeworkTitle')
    rubrics = data.get('rubrics')

    # Update the rubrics in the database
    try:
        result = client['fyp']['assignment'].update_one(
            {'class': class_name, 'title': homework_title},
            {'$set': {'rubrics': rubrics}}
        )
        if result.modified_count > 0:
            return jsonify({'message': 'Rubrics updated successfully'}), 200
        else:
            return jsonify({'message': 'No updates made to the rubrics'}), 200
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while updating rubrics'}), 500

def get_submitted_work_by_studentid_and_assignmentid(client, student_id, assignment_id):
    work = client['fyp']['submittedWork'].find_one({'studentId': student_id, 'assignmentId': assignment_id})
    return work

def to_get_class_by_assignment(client, assignment_id):
    assignment = client['fyp']['assignment'].find_one({"_id": ObjectId(assignment_id)})
    if assignment:
        return jsonify({
            'class': assignment['class']
        })
    else:
        return jsonify('No assignment found'), 404

def to_get_title_by_assignment(client, assignment_id):
    assignment = client['fyp']['assignment'].find_one({"_id": ObjectId(assignment_id)})
    if assignment:
        return jsonify({
            'title': assignment['title']
        })
    else:
        return jsonify('No assignment found'), 404

def to_get_homework_text_by_submissionId(client, submission_id):
    submission = client['fyp']['submittedWork'].find_one({"_id": ObjectId(submission_id)})
    if submission:
        return jsonify({
            'homeworkText': submission['ocrText'],"status": "success"
        })
    else:
        return jsonify('No submission found'), 404

def to_get_student_submissions(client, student_id):
    submissions_collection = client['fyp']['submittedWork']
    assignments_collection = client['fyp']['assignment']

    # Find all submissions for the student
    submissions = submissions_collection.find({"studentId": str(student_id)})

    # Fetch the title of each assignment for which the student has submitted work
    submitted_assignment_titles = []
    for submission in submissions:
        assignment_id = submission.get("assignmentId")
        if assignment_id:
            assignment = assignments_collection.find_one({"_id": ObjectId(assignment_id)})
            if assignment:
                submitted_assignment_titles.append(assignment.get("title", "No Title"))

    return jsonify(submitted_assignment_titles)


def to_get_students_for_homework(client,assignmentTitle):
    assgnmentId= client['fyp']['assignment'].find_one({'title':assignmentTitle})['_id']
    submitted_work_collection = client['fyp']['submittedWork']
    students_collection = client['fyp']['student']

    # Find all submissions for the given assignment
    submissions = submitted_work_collection.find({"assignmentId": str(assgnmentId)})

    # Create a list to store student details along with their submission ID
    student_submissions = []

    # Iterate over the submissions to fetch corresponding student details
    for submission in submissions:
        student_id = submission.get('studentId')
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            student_submissions.append({
                "name": student.get('name'),
                "submissionId": str(submission.get('_id')),  # Convert ObjectId to string
                "studentId": str(student_id),  # Convert ObjectId to string
                "number": student.get('number')
            })

    print (student_submissions)

    return jsonify(student_submissions)