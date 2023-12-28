import json
from flask_cors import CORS

from flask import Flask, request
from werkzeug.utils import secure_filename
import os

from src.CompareResultEncoder import CompareResultEncoder
from src.DatReader import DatReader
from src import Profile
from run import Comparator

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = './uploads'


def get_file_path(filename: str) -> str:
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


@app.route("/", methods=['POST'])
def run():
    threshold = float(request.values.get("threshold"))
    allow_err_count = int(request.values.get("allow_err_count"))
    decimal_points = json.loads(request.values.get("decimal_points"))
    numeric_columns = json.loads(request.values.get("numeric_columns"))
    phase_name_col = request.values.get("phase_name_col")

    profile = Profile(
        numeric_columns=numeric_columns,
        phase_column=phase_name_col,
        threshold=threshold,
        allow_err_count=allow_err_count,
        decimal_points=decimal_points
    )
    # try:
    figure1 = request.files['figure1']
    figure2 = request.files['figure2']
    figure1_filename = secure_filename(figure1.filename)
    figure2_filename = secure_filename(figure2.filename)
    figure1.save(os.path.join(app.config['UPLOAD_FOLDER'], figure1_filename))
    figure2.save(os.path.join(app.config['UPLOAD_FOLDER'], figure2_filename))

    comparator = Comparator(profile=profile)
    comparator.threshold = threshold
    comparator.allow_err_count = allow_err_count
    comparator.decimal_points = decimal_points
    response = comparator.check(get_file_path(figure1_filename),
                                get_file_path(figure2_filename))
    # status = 200 if response else 400
    return CompareResultEncoder().encode(response), 200, {"Content-Type": "application/json"}


@app.route("/transfer", methods=['POST'])
def transfer():
    figure1 = request.files['figure1']
    figure1_filename = secure_filename(figure1.filename)
    figure1.save(os.path.join(app.config['UPLOAD_FOLDER'], figure1_filename))
    reader = DatReader(get_file_path(figure1_filename))
    response = {
        "columns": reader.get_headers(),
        "list": reader.data.fillna(0).to_dict(orient="records")
    }
    return json.dumps(response), 200, {
        "Content-Type": "application/json"
    }
