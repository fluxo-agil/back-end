import os
from flask import Flask, flash, request, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
from app.extract import *
from app.process import *

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return "Hello world!"


@app.route("/process", methods=['POST'])
def process_recommendation():
    if request.method == 'POST' or file.filename == '':
        if 'file' not in request.files:
            return 'No file to upload'
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            approved_courses = get_approved_courses(file_path)
            program_id = get_program_id(file_path)

            missing_courses = get_missing_courses(program_id, approved_courses)
            n, p, u, c, S = get_process_structure(missing_courses)

            recommendation = process(n, p, u, c, S, missing_courses)

            return jsonify(recommendation)
    return ''


if __name__ == "__app__":
    app.run()
