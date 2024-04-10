from bson import ObjectId
from flask import jsonify, request

from models.assignment import to_get_rubrics_by_assignment, to_get_description_by_assignment, \
    get_submitted_work_by_studentid_and_assignmentid
from models.marking_gpt import gpt_mark
from models.student import get_students_by_class


def mark_and_save_marking(client):
    data = request.get_json()
    assignment_id = data['assignmentId']
    class_name = data['class']
    students= client['fyp']['student'].find({'class': class_name})

    assignment = client['fyp']['assignment'].find_one({'_id': ObjectId(assignment_id)})

    rubrics =client['fyp']['assignment'].find_one({"_id": ObjectId(assignment_id)})['rubrics']
    description=client['fyp']['assignment'].find_one({"_id": ObjectId(assignment_id)})['description']

    for student in students:
        student_id = student['_id']
        student_work= client['fyp']['submittedWork'].find_one({'studentId': str(student_id), 'assignmentId': str(assignment_id)})['ocrText']
        markings=gpt_mark(student_work, rubrics, description )
        #print (client['fyp']['student'].find_one({'_id': ObjectId(student_id)})['name'])


        # Splitting the response into lines for easier processing
        lines = markings.strip().split('\n')

        # Initialize variables to store the extracted score and explanation
        extracted_score = None
        extracted_explanation = None

        # Parsing each line to find the score and explanation
        for line in lines:
            if line.startswith("Score:"):
                # Extracting the score
                extracted_score = line.replace("Score:","").strip()
            elif line.startswith("Explanation:"):
                # Extracting the explanation
                extracted_explanation = line.replace("Explanation:","").strip()

        client['fyp']['submittedWork'].update_one(
            {'studentId': str(student_id), 'assignmentId': str(assignment_id)},
            {'$set': {'marking': {'score': extracted_score, 'explanation': extracted_explanation}}}
        )

        # print(f"Score: {extracted_score}")
        # print(f"Explanation: {extracted_explanation}")
    return jsonify({'message': 'Marking completed successfully'}), 200


def get_grades_by_assignment(client, assignment_id):
    # Convert assignment_id to ObjectId since it is stored as an ObjectId in MongoDB

    # Fetching grades data for the given assignment
    submissions = client['fyp']['submittedWork'].find({'assignmentId': str(assignment_id)})
    # Creating a list of scores and explanations
    grades_list = []
    for submission in submissions:
        # Only proceed if marking information is present

        if 'marking' in submission:
            grade_data = {
                'submissionId': str(submission['_id']),  # Convert ObjectId to string
                'studentId': str(submission['studentId']),
                'studentName': client['fyp']['student'].find_one({'_id': ObjectId(submission['studentId'])})['name'],
                'studentNumber': client['fyp']['student'].find_one({'_id': ObjectId(submission['studentId'])})['number'],
                'score': submission['marking'].get('score'),
                'explanation': submission['marking'].get('explanation')
                # Providing default if not found
            }
            grades_list.append(grade_data)

    # Return the list of scores and explanations as JSON
    return jsonify(grades_list)


def to_update_grade(client, submission_id):
    # Get the data from the request's body
    data = request.get_json()
    print(data)

    try:
        # Extract data
        #submission_id = ObjectId(data.get('submissionId'))
        new_score = data.get('score')
        new_explanation = data.get('explanation')

        print(new_score)
        print(new_explanation)

        # Find the document and update it
        result = client['fyp']['submittedWork'].update_one(
            {'_id': ObjectId(submission_id)},
            {'$set': {
                'marking.score': new_score,
                'marking.explanation': new_explanation
            }}
        )
        print(result)

        # Check if the database update was successful
        if result.modified_count == 1:
            print('modified')
            return jsonify({'success': True, 'message': 'Grade updated successfully'}), 200
        else:
            print('not modified')
            return jsonify({'success': False, 'message': 'No document found or data was the same'}), 404

    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred'}), 500


