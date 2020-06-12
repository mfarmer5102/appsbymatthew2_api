# General imports
from flask import Flask, Blueprint, request, jsonify
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json

# Define database
myclient = pymongo.MongoClient(os.getenv('DB_URL', "mongodb://localhost:27017"))
database = myclient[(os.getenv('DB_NAME', "local-database-name"))]

# Define collections
skillsCollection = database["skills"]

# Define blueprint
Skills = Blueprint('Skills', __name__)

# Define reusable functions

def bsonToJson(item):
    return json.loads(json_util.dumps(item))

def jsonResponse(dataset):
    arr = []
    for item in dataset:
        arr.append(bsonToJson(item))
    return json.dumps(arr)

# Begin routes

@Skills.route("/api/skills", methods=['GET', 'POST', 'PUT', 'DELETE'])
def sendKeywords():

    if request.method == 'GET':
        dataset = skillsCollection.find().sort([("type", pymongo.ASCENDING), ("name", pymongo.ASCENDING)])
        return jsonResponse(dataset)
    
    if request.method == 'POST':
        skillsCollection.insert_one(request.json)
        return jsonify(
            code=200,
            msg="Success"
        )

    if request.method == 'PUT':
        myquery = {'_id': ObjectId(request.json['_id'])}
        skillsCollection.replace_one(myQuery, request.json, upsert=True)
        return jsonify(
            code=200,
            msg="Success"
        )

    if request.method == 'DELETE':
        skillsCollection.delete_one({'_id': ObjectId(request.json['_id'])})
        return jsonify(
            code=200,
            msg="Success"
        )