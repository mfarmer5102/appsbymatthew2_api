from flask import jsonify
import os
from bson import json_util
import json


# Functions
def bson_to_json(item):
    return json.loads(json_util.dumps(item))


def json_response(dataset):
    arr = []
    for item in dataset:
        arr.append(bson_to_json(item))
    return json.dumps(arr)


def flatten_mongo_ids(dataset):
    formatted_arr = []
    for datum in dataset:
        datum["_idFlat"] = str(datum["_id"])
        formatted_arr.append(datum)
    return formatted_arr


def is_authenticated_user(request):
    if request.headers.get('user-token') != os.getenv('SECRET_TOKEN', 'mysecrettoken'):
        return False
    else:
        return True


def handle_unauthenticated_request():
    return jsonify(
        code=401,
        msg="Unauthorized"
    ), 401


def handle_successful_write_request():
    return jsonify(
        code=200,
        msg="Success"
    )