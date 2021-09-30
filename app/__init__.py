import os
import sys
sys.path.append(os.path.abspath("./extract_pdf_data"))
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from extract import extrair_materias_aprovado,extrair_numero_curriculo

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

@app.route("/upload-pdf", methods=['POST'])
def process():
  if request.method == 'POST' or file.filename == '':
    if 'file' not in request.files:
      return 'No file to upload'
    file = request.files['file']
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      file.save(file_path)
      materias_aprovado = extrair_materias_aprovado(file_path)
      numero_curriculo =  extrair_numero_curriculo(file_path)
      return 'File uploaded successfully:'
  return ''


if __name__ == "__app__":
  app.run()