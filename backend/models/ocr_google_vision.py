import os
import random
import json

from flask import request, jsonify
from google.cloud import vision
from google.cloud import storage
from werkzeug.utils import secure_filename

from models.assignment import save_text_to_db
from dotenv import load_dotenv

load_dotenv()

storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()

bucket_name = os.environ.get('BUCKET_NAME')
os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def to_upload_and_process_pdf(client):
    bucket = storage_client.get_bucket(bucket_name)
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Upload file to Google Cloud Storage
        blob = bucket.blob(filename)
        blob.upload_from_string(file.read(), content_type='application/pdf')

        # Process file with Vision API
        gcs_source_uri = f'gs://{bucket_name}/{filename}'
        text = process_with_vision_api(gcs_source_uri)

        # Here you would save 'text' to your database associated with the student
        student_id = request.form.get('student_id')
        assignment_id = request.form.get('assignment_id')  # Get the assignment ID from the request
        save_text_to_db(client,student_id, assignment_id, text)

        return jsonify({'message': 'File processed', 'text': text, 'status':'success'})

    return jsonify({'error': 'Error processing file'}), 400

def process_with_vision_api(gcs_source_uri):
    # Set where to store the results of the OCR
    # random 6 digists
    randomId = str(random.randint(100000, 999999))
    output_uri = f'gs://{bucket_name}/{randomId}-output/'

    async_request = vision.AsyncAnnotateFileRequest(
        features=[vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)],
        input_config=vision.InputConfig(
            gcs_source=vision.GcsSource(uri=gcs_source_uri),
            mime_type='application/pdf'
        ),
        output_config=vision.OutputConfig(
            gcs_destination=vision.GcsDestination(uri=output_uri),
            batch_size=5
        )
    )

    operation = vision_client.async_batch_annotate_files(requests=[async_request])
    result = operation.result(timeout=180)

    # The result does not contain the OCR text directly. It indicates that the operation was completed.
    # You need to fetch the result files from the output_urimId}/o
    # Assuming the results are stored in a single output file for simplicity. In practice, you might have multiple files.
    # list all blob in a bucket
    blist = storage_client.bucket(bucket_name).list_blobs(prefix=f'{randomId}-output')
    blist = list(blist)
    output_blob = blist[0]
    # output_blob = storage_client.bucket(bucket_name).blob(f'{randomId}-output/output-1-to-1.json')
    json_string = output_blob.download_as_string()
    response = json.loads(json_string)

    # Extract text from the response
    output_text = ''
    for page_response in response['responses']:
        output_text += page_response.get('fullTextAnnotation', {}).get('text', '')

    return output_text

