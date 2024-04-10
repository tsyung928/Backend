from flask import Flask, jsonify, request
from bson import ObjectId

def get_average_grades_by_class(client, class_id):
    # Find all assignments for the class
    assignments = list(client['fyp']['assignment'].find({"class": class_id}))

    # Initialize a list to hold the average grade for each assignment
    assignment_averages = []

    for assignment in assignments:
        # Find all submitted work for this assignment
        submissions = list(client['fyp']['submittedWork'].find({"assignmentId": str(assignment['_id'])}))

        # Calculate the average grade for the assignment
        total_score = 0
        num_submissions = 0
        for submission in submissions:
            # Ensure that score is an integer before adding
            score = int(submission['marking']['score'])
            total_score += score
            num_submissions += 1

        # Avoid division by zero
        average_score = total_score / num_submissions if num_submissions > 0 else 0
        assignment_averages.append({
            "name": assignment.get("title", "Unknown Assignment"),
            "averageGrade": average_score
        })

    if assignment_averages:
        return jsonify(assignment_averages)
    else:
        return jsonify({"error": "No assignments found for the class"}), 404


def to_get_top_performing_students(client, class_id):
    assignments_collection = client['fyp']['assignment']
    submitted_work_collection = client['fyp']['submittedWork']
    students_collection = client['fyp']['student']
    TOP_STUDENTS_LIMIT = 2

    # Find the assignment IDs for the class
    assignments = assignments_collection.find({"class": class_id})
    assignment_ids = [assignment['_id'] for assignment in assignments]

    # Fetch all the submissions for these assignments
    submissions = []
    for assignment_id in assignment_ids:
        # Iterate over the cursor to extend the submissions list with actual documents
        submissions.extend(list(submitted_work_collection.find({"assignmentId": str(assignment_id)})))

    print (submissions)
    # Calculate the average mark for each student
    student_scores = {}
    for submission in submissions:
        student_id = submission['studentId']
        score = float(submission['marking']['score'])  # Convert score to float
        if student_id in student_scores:
            student_scores[student_id].append(score)
        else:
            student_scores[student_id] = [score]

    # Calculate average scores
    for student_id, scores in student_scores.items():
        student_scores[student_id] = sum(scores) / len(scores)

    # Sort students by average score
    top_students_ids = sorted(student_scores, key=student_scores.get, reverse=True)[:TOP_STUDENTS_LIMIT]

    # Fetch student names
    top_students = []
    for student_id in top_students_ids:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            top_students.append({
                "name": student['name'],
                "score": student_scores[student_id]
            })
    print(top_students)

    return jsonify(top_students)

def to_get_low_performing_students(client, class_id):
    assignments_collection = client['fyp']['assignment']
    submitted_work_collection = client['fyp']['submittedWork']
    students_collection = client['fyp']['student']
    LOW_STUDENTS_LIMIT = 2

    # Find the assignment IDs for the class
    assignments = assignments_collection.find({"class": class_id})
    assignment_ids = [assignment['_id'] for assignment in assignments]

    # Fetch all the submissions for these assignments
    submissions = []
    for assignment_id in assignment_ids:
        # Iterate over the cursor to extend the submissions list with actual documents
        submissions.extend(list(submitted_work_collection.find({"assignmentId": str(assignment_id)})))

    # Calculate the average mark for each student
    student_scores = {}
    for submission in submissions:
        student_id = submission['studentId']
        score = float(submission['marking']['score'])  # Convert score to float
        if student_id in student_scores:
            student_scores[student_id].append(score)
        else:
            student_scores[student_id] = [score]

    # Calculate average scores
    for student_id, scores in student_scores.items():
        student_scores[student_id] = sum(scores) / len(scores)

    # Sort students by average score in ascending order
    low_students_ids = sorted(student_scores, key=student_scores.get)[:LOW_STUDENTS_LIMIT]

    # Fetch student names
    low_students = []
    for student_id in low_students_ids:
        student = students_collection.find_one({"_id": ObjectId(student_id)})
        if student:
            low_students.append({
                "name": student['name'],
                "score": student_scores[student_id]
            })

    return jsonify(low_students)
