import json
from typing import List

from flask_cors import CORS

from flask import Flask, request
from werkzeug.utils import secure_filename
import os

from src.CompareResultEncoder import CompareResultEncoder
from src.DatReader import DatReader
from run import Comparator
from src.Profile import Profile

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

folder = os.path.exists(app.config['UPLOAD_FOLDER'])

if not folder:
    os.makedirs(app.config['UPLOAD_FOLDER'])


def get_file_path(filename: str) -> str:
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)


@app.route("/single", methods=['POST'])
def single():
    threshold = float(request.values.get("threshold"))
    allow_err_count = int(request.values.get("allow_err_count"))
    decimal_points = json.loads(request.values.get("decimal_points"))
    reg_list = json.loads(request.values.get("reg_list"))
    phase_name_col = request.values.get("phase_name_col")

    profile = Profile(
        force_numeric_columns=reg_list,
        phase_column=phase_name_col,
        threshold=threshold,
        allow_err_count=allow_err_count,
        decimal_points=decimal_points
    )
    # try:
    print(request.files)
    figure1 = request.files['figure1']
    figure2 = request.files['figure2']
    figure1_filename = secure_filename(figure1.filename)
    figure2_filename = secure_filename(figure2.filename)
    figure1.save(os.path.join(app.config['UPLOAD_FOLDER'], figure1_filename))
    figure2.save(os.path.join(app.config['UPLOAD_FOLDER'], figure2_filename))

    comparator = Comparator(profile=profile)
    response = comparator.check(get_file_path(figure1_filename),
                                get_file_path(figure2_filename))
    # status = 200 if response else 400
    return CompareResultEncoder().encode(response), 200, {"Content-Type": "application/json"}


@app.route("/multiple", methods=['POST'])
def multiple():
    figure1s: List = request.files.getlist("figure1s[]")
    figure2s: List = request.files.getlist("figure2s[]")
    threshold: float = float(request.values.get("threshold"))
    allow_err_count: int = int(request.values.get("allow_err_count"))
    decimal_point: int = int(request.values.get("decimal_point"))
    reg_list: List[str] = json.loads(request.values.get("reg_list"))
    phase_name_col: str = request.values.get("phase_name_col")

    profile = Profile(
        reg_list=reg_list,
        phase_column=phase_name_col,
        threshold=threshold,
        allow_err_count=allow_err_count,
        decimal_point=decimal_point
    )
    print("Profile ready.")
    try:
        # try:
        figure1s: List = request.files.getlist("figure1s[]")
        figure2s: List = request.files.getlist("figure2s[]")
        figure1s_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'figure1s')
        figure2s_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'figure2s')
        compare_filenames = []
        for figure1 in figure1s:
            print(figure1.filename)
            figure1_filename = secure_filename(os.path.basename(figure1.filename))
            figure1.save(os.path.join(figure1s_folder, figure1_filename))
            compare_filenames.append(figure1_filename)
        for figure2 in figure2s:
            figure2_filename = secure_filename(os.path.basename(figure2.filename))
            figure2.save(os.path.join(figure2s_folder, figure2_filename))

        response_list = []
        for filename in compare_filenames:
            comparator = Comparator(profile=profile)
            figure1_path = os.path.join('figure1s', filename)
            figure2_path = os.path.join('figure2s', filename)
            response = comparator.check(get_file_path(figure1_path), get_file_path(figure2_path))
            response_list.append({
                'filename': filename,
                'report': response
            })
        # status = 200 if response else 400
        return CompareResultEncoder().encode(response_list), 200, {"Content-Type": "application/json"}

    except Exception as e:
        print(e)
        return json.dumps({
            "message": "服务器错误"
        }), 500, {
            "Content-Type": "application/json"
        }


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
