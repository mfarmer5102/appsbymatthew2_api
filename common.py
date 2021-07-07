# General imports
from flask import Flask, Blueprint, request, jsonify, Response
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json
import datetime

# Variables
myclient = pymongo.MongoClient(os.getenv('DB_URL', "mongodb://localhost:27017"))
database = myclient[(os.getenv('DB_NAME', "appsbymatthew_dev"))]

# Functions
def bsonToJson(item):
    return json.loads(json_util.dumps(item))

def jsonResponse(dataset):
    arr = []
    for item in dataset:
        arr.append(bsonToJson(item))
    return json.dumps(arr)

def flattenMongoIds(dataset):
    formattedArr = []
    for datum in dataset:
        datum["_idFlat"] = str(datum["_id"])
        formattedArr.append(datum)
    return formattedArr

def isAuthenticatedUser(request):
    if request.headers.get('user-token') != os.getenv('SECRET_TOKEN', 'mysecrettoken'):
        return False
    else:
        return True
        
def handleUnauthenticatedRequest():
    return jsonify(
        code=401,
        msg="Unauthorized"
    ), 401

def handleSuccessfulWriteRequest():
    return jsonify(
            code=200,
            msg="Success"
        )