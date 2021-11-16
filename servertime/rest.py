from datetime import datetime
from flask import Flask, jsonify, request, make_response, abort

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
    # _assert("date" in data, 400, "Activity without date filed")
    # _assert("beginning" in data, 400, "Activity without beginning filed")

    name = data.get("name")
    # date = data.get("date")
    # beginning = data.get("beginning")
    description = data.get("description", "")

    try:
        activity = controller.create_activity(name=name, description=description)
    except AssertionError as e:
        _abort(400, str(e))
    res = {
        "activity": activity,
        "status_code": 201
    }

    return jsonify(res), 201


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response
