import os
from flask import Flask, flash, request, redirect, url_for, jsonify, json
from collections import defaultdict
from werkzeug.utils import secure_filename
from app.extract import *
from app.process import *
from flask_cors import CORS

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

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
            return jsonify({
                'error': 'No file to upload'
            }), 400
        file = request.files['file']

        max_credits_by_period = request.form.get("max_credits_by_period", 24)
        if max_credits_by_period:
            max_credits_by_period = int(max_credits_by_period)

        optional_courses = request.form.get("optional_courses", None)
        if optional_courses:
            optional_courses = json.loads(optional_courses)

        courses_with_specific_period = request.form.get(
            "courses_with_specific_period", None)
        if courses_with_specific_period:
            courses_with_specific_period = json.loads(
                courses_with_specific_period)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                approved_courses = get_approved_courses(file_path)
                program_id = get_program_id(file_path)

            except:
                return jsonify({
                    'error': 'Falha ao extrair dados do PDF'
                }), 400

            try:
                missing_courses = get_missing_courses(
                    program_id, approved_courses, optional_courses)
                n, p, u, c, S = get_process_structure(
                    missing_courses, max_credits_by_period)
                recommendation = process(n, p, u, c, S, missing_courses)
            except:
                return jsonify({
                    'error': 'Falha no processamento da recomendação'
                }), 400

            os.remove(UPLOAD_FOLDER + '/' + filename)

            return jsonify(recommendation)
    return jsonify({
        'error': 'File format not allowed'
    }), 400


if __name__ == "__app__":
    app.run()
