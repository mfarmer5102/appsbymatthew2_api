# General imports
from flask import Flask, Blueprint, request, jsonify
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json

# Define database
myclient = pymongo.MongoClient(os.getenv('DB_URL', "mongodb://localhost:27017"))
database = myclient[(os.getenv('DB_NAME', "appsbymatthew_dev"))]

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
        myRequest = request.json
        myRequest['is_proficient'] = True if request.json['is_proficient'] == 'true' else False
        skillsCollection.insert_one(myRequest)
        print(myRequest)
        return jsonify(
            code=200,
            msg="Success"
        )

    if request.method == 'PUT':
        incomingId = request.json['_id']
        print(incomingId['$oid'])
        myQuery = {'_id': ObjectId(incomingId['$oid'])}
        print(myQuery)
        myRequestWithoutId = request.json
        myRequestWithoutId['is_proficient'] = True if request.json['is_proficient'] == 'true' else False
        print(myRequestWithoutId)
        del myRequestWithoutId['_id']
        skillsCollection.replace_one(myQuery, myRequestWithoutId, upsert=True)
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

@Skills.route("/api/skills/one", methods=['GET'])
def sendFilteredKeywords():

    # Prepare the find object
    #########################

    findObj = {}

    # Document ID
    suppliedId = request.args.get("id")
    if suppliedId is not None:
        findObj["_id"] = ObjectId(suppliedId)

    # Skill Code
    suppliedCode = request.args.get("skillCode")
    if suppliedCode is not None:
        findObj["code"] = suppliedCode

    # Demonstrable
    isDemonstrable = request.args.get("demonstrable")
    if isDemonstrable is not None:
        findObj["showOnPortfolio"] = request.args.get("demonstrable") == "true"

    # Proficient
    isProficient = request.args.get("proficient")
    if isProficient is not None:
        findObj["showInGallery"] = request.args.get("proficient") == "true"

    # Prepare the sort object
    #########################

    sortArr = []
    
    # Name
    sortName = request.args.get("sortName")
    if sortName is not None:
        sortArr.append(("name", pymongo.ASCENDING if request.args.get("sortName") == "asc" else pymongo.DESCENDING))

    # Type
    sortType = request.args.get("sortType")
    if sortType is not None:
        sortObj.append(("type", pymongo.ASCENDING if request.args.get("sortName") == "asc" else pymongo.DESCENDING))
    
    # Default
    if not sortArr: # Mongo query won't work if the sort array is empty, so give it something to sort on
        sortArr.append(("name", pymongo.ASCENDING))

    # Make the DB Query
    #########################

    dataset = skillsCollection.find(findObj).sort(sortArr)
    return jsonResponse(dataset)
