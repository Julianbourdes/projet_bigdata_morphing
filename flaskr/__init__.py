import os

from flask import Flask, jsonify
from flask import (flash, redirect, request, url_for, send_from_directory)
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './flaskr/static/uploaded_images'
OUTPUT_FOLDER = './flaskr/static/output_gif'
MORPH_FRAMES = './flaskr/static/morph_frames'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_envvar('.env', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if not os.path.isdir(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.isdir(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    if not os.path.isdir(MORPH_FRAMES):
        os.makedirs(MORPH_FRAMES)

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/upload', methods=['POST'])
    def upload_file():
        print(request)
        # check if the post request has the file part
        if 'first_choice' not in request.files:
            resp = jsonify({'message': 'Pas de fichier'})
            resp.status_code = 400
            return resp

        file = request.files['first_choice']

        errors = {}
        success = False

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            registered_filename = "image_upload." + filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(UPLOAD_FOLDER, registered_filename))
            success = True
        else:
            errors[file.filename] = 'Ce type de fichier n\'est pas autorisé'

        if success and errors:
            errors['message'] = 'Le fichier a bien été chargé'
            resp = jsonify(errors)
            resp.status_code = 206
            return resp
        if success:
            resp = jsonify({'message': 'Le fichier a bien été chargé'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 400
            return resp

    @app.route('/uploads/<name>')
    def download_file(name):
        return send_from_directory(app.config["OUTPUT_FOLDER"], name)

    from . import morphing
    app.register_blueprint(morphing.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)

    return app
