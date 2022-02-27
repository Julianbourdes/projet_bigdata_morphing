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

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'first_choice' not in request.files:
                flash('No file part')
            file = request.files['first_choice']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            print(file.mimetype_params)
            if file.filename == '':
                flash('No selected file')
            if file and allowed_file(file.filename):
                print('toto')
                filename = secure_filename(file.filename)
                print(filename)
                registered_filename = "image_upload." + filename.rsplit('.', 1)[1].lower()
                print(registered_filename)
                file.save(os.path.join(UPLOAD_FOLDER, registered_filename))
        return jsonify({"Image Uploaded" : registered_filename})

    @app.route('/uploads/<name>')
    def download_file(name):
        return send_from_directory(app.config["OUTPUT_FOLDER"], name)

    from . import morphing
    app.register_blueprint(morphing.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule(
        "/uploads/<name>", endpoint="download_file", build_only=True
    )
    app.add_url_rule('/upload', endpoint="upload_file", build_only=True)

    return app
