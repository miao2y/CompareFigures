import json

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from run import check

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './uploads'


@app.route("/", methods=['POST'])
def run():
    # try:
    figure1 = request.files['figure1']
    figure2 = request.files['figure2']
    figure1_filename = secure_filename(figure1.filename)
    figure2_filename = secure_filename(figure2.filename)
    figure1.save(os.path.join(app.config['UPLOAD_FOLDER'], figure1_filename))
    figure2.save(os.path.join(app.config['UPLOAD_FOLDER'], figure2_filename))
    res, message = check(os.path.join(app.config['UPLOAD_FOLDER'], figure1_filename),
                         os.path.join(app.config['UPLOAD_FOLDER'], figure2_filename))
    data = {
        "success": res,
        "message": message
    }
    status = 200 if res else 400
    return json.dumps(data), status, {"Content-Type": "application/json"}