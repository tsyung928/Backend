from flask import jsonify


def get_student_by_name(client, name):
    return client['fyp']['student'].find_one({'name': name})

def create_student(client, name, age):
    return client['fyp']['student'].insert_one({"name": name, "age": age})

def get_students_by_class(client, class_name):
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

def to_get_all_students_list(client):
    students = list(
        client['fyp']['student'].find({}, {'_id': 1, 'name': 1, 'class': 1, 'number': 1}))

    for student in students:
        student['_id'] = str(student['_id'])

    return jsonify(students)
