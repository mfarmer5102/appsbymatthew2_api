# General imports
from flask import Flask, Blueprint, request, jsonify, Response
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json
import datetime
import certifi

# Variables
my_client = pymongo.MongoClient(os.getenv('MONGO_INSTANCE_URL', "mongodb://localhost:27017"), tlsCAFile=certifi.where())
database = my_client["apps_by_matthew"]


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
