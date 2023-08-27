import os
from flask import send_from_directory, render_template, Response, make_response, \
    Flask, flash, request, redirect, url_for, after_this_request, jsonify, abort, g
from flask_cors import CORS
import glob
from group_formation import form_groups
from uuid import uuid4
import threading

CSV_FILE_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['CSV_FILE_FOLDER'] = CSV_FILE_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
CORS(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/check', methods=['POST'])
def check_file():
    @after_this_request
    def after_request(response):
        if g.to_delete:
            fileList = glob.glob(os.path.join(app.config['CSV_FILE_FOLDER'], g.uuid + "*.csv"))
            for file in fileList:
                os.remove(file)

        return response

    data = request.get_json(force=True)
    uuid = data['uuid'];
    g.uuid = uuid
    output_file_name = uuid + '_output.csv'

    if os.path.exists(os.path.join(app.config['CSV_FILE_FOLDER'], output_file_name)):
        g.to_delete = True

        return send_from_directory(app.config['CSV_FILE_FOLDER'], output_file_name, as_attachment=True)

    g.to_delete = False
    response = make_response( 'processing...', 202)

    return response

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return Response(
                "File not uploaded",
                status=400,
            )

    input_file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if input_file.filename == '':
        return Response(
                "File not uploaded",
                status=400,
            )

    if not allowed_file(input_file.filename):
        return Response(
                "format not csv file",
                status=400,
            )

    if input_file and allowed_file(input_file.filename):
        uuid = str(uuid4())
        input_file_name = uuid + '_input.csv'
        input_file_path = os.path.join(app.config['CSV_FILE_FOLDER'], input_file_name)
        input_file.save(input_file_path)
        group_num = int(request.form['group_num'])
        algorithm_type = request.form['algorithm_type']
        print(algorithm_type)
        thread = threading.Thread(
            target=form_groups,
            args=(app.config['CSV_FILE_FOLDER'], group_num, uuid, algorithm_type),
            daemon=True
        )
        thread.start()
        response = make_response(
                jsonify(
                    {"uuid": uuid}
                ),
                200,
            )
        response.headers["Content-Type"] = "application/json"

        return response

if __name__ == "__main__":
    app.run()
