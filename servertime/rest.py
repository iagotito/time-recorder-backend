import os
from datetime import datetime
from flask import Flask, jsonify, request, make_response, abort, send_file

from . import controller

app = Flask(__name__)


def _abort(status_code, message):
    res = {
        "message": message,
        "status_code": status_code
    }
    response = make_response(jsonify(res), status_code)
    abort(response)


def _assert(condition, status_code, message):
    if condition: return
    _abort(status_code, message)


@app.route("/status")
def status():
    status = {
        "status": "running",
    }
    return jsonify(status), 200


# @app.route("/activity/<id>", methods=["GET"])
# def get_activity(id):
    # try:
        # activity = controller.get_activity(id)
    # except AssertionError as e:
        # _abort(400, str(e))
    # res = {
        # "activity": activity,
        # "status_code": 200
    # }
    # return jsonify(res), 200


@app.route("/activities", methods=["GET"])
def get_activities():
    args = request.args

    date:str = args.get("date", datetime.now().strftime("%Y-%m-%d"))

    activities = controller.get_activities(date)

    res = {
        "activities": activities,
        "status_code": 200
    }
    return jsonify(res), 200


@app.route("/activities", methods=["POST"])
def post_activity():
    data = request.get_json()
    if data is None:
        _abort(400, "No request body")

    _assert("name" in data, 400, "Activity without name filed")

    name = data.get("name")
    description = data.get("description", "")

    finished_activity = None
    new_activity = None
    if name == "end":
        try:
            finished_activity = controller.finish_last_activity()
        except AssertionError as e:
            _abort(400, str(e))

        res = {
            "new_activity": new_activity,
            "finished_activity": finished_activity,
            "status_code": 200
        }
        return jsonify(res), 200
    else:
        try:
            new_activity, finished_activity = controller.create_activity(name=name, description=description)
        except AssertionError as e:
            _abort(400, str(e))

        res = {
            "new_activity": new_activity,
            "finished_activity": finished_activity,
            "status_code": 201
        }
        return jsonify(res), 201


@app.route("/activity/<id>", methods=["PUT"])
def put_activity(id):
    data = request.get_json()
    if data is None:
        _abort(400, "No request body")

    updated_activity = None
    try:
        updated_activity = controller.update_activity(id, data)
    except AssertionError as e:
        _abort(400, str(e))

    res = {
        "updated_activity": updated_activity,
        "status_code": 200
    }
    return jsonify(res), 200


@app.route("/download", methods=["GET"])
def download_data():
    args = request.args

    date:str = args.get("date", datetime.now().strftime("%Y-%m-%d"))

    filename = controller.create_csv_data(date)
    filepath = os.path.abspath(filename)

    return send_file(filepath, as_attachment=True), 200


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response
