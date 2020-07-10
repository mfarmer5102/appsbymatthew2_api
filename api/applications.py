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
applicationsCollection = database["apps"]

# Define blueprint
Applications = Blueprint('Applications', __name__)

# Define reusable functions

def bsonToJson(item):
    return json.loads(json_util.dumps(item))

def jsonResponse(dataset):
    arr = []
    for item in dataset:
        arr.append(bsonToJson(item))
    return json.dumps(arr)

# Begin routes

@Applications.route("/api/applications", methods=['GET', 'POST', 'PUT', 'DELETE'])
def sendApplications():

    if request.method == 'GET':
        dataset = applicationsCollection.find().sort([("isFeatured", pymongo.DESCENDING), ("publishDate", pymongo.DESCENDING) ])
        return jsonResponse(dataset)

    if request.method == 'POST':
        applicationsCollection.insert_one(request.json)
        return jsonify(
            code=200,
            msg="Success"
        )

    if request.method == 'PUT':
        myquery = {'_id': ObjectId(request.json['_id'])}
        applicationsCollection.replace_one(myQuery, request.json, upsert=True)
        return jsonify(
            code=200,
            msg="Success"
        )

    if request.method == 'DELETE':
        applicationsCollection.delete_one({'_id': ObjectId(request.json['_id'])})
        return jsonify(
            code=200,
            msg="Success"
        )

@Applications.route("/api/applications/filter", methods=['GET'])
def sendFilteredApplications():

    # Prepare the find object
    #########################

    findObj = {}

    # Featured
    isFeatured = request.args.get("featured")
    if isFeatured is not None:
        findObj["isFeatured"] = request.args.get("featured") == "true"

    # Utilized Skills
    keywords = request.args.get("keywords")
    if keywords is not None:
        suppliedKeywords = request.args.get("keywords")
        parsedKeywords = suppliedKeywords.split(',')
        findObj["keywords"] = {"$all": parsedKeywords}
    
    print(findObj)
    # Prepare the sort object
    #########################

    sortArr = []
    
    # Date
    sortDate = request.args.get("sortDate")
    if sortDate is not None:
        sortArr.append(("publishDate", pymongo.DESCENDING if request.args.get("sortDate") == "desc" else pymongo.ASCENDING))

    # Default
    if not sortArr: # Mongo query won't work if the sort array is empty, so give it something to sort on
        sortArr.append(("publishDate", pymongo.DESCENDING))

    # Make the DB Query
    #########################

    dataset = applicationsCollection.find(findObj).sort(sortArr)
    return jsonResponse(dataset)
