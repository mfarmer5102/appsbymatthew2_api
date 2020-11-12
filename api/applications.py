# General imports
from flask import Flask, Blueprint, request, jsonify
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json

# Define database
myclient = pymongo.MongoClient("mongodb+srv://mfarmer5102:phoebe17@cluster0.ya0ol.mongodb.net/AppGalleryLite?retryWrites=true&w=majority")
database = myclient["AppGalleryLite"]

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

@Applications.route("/api/applications/countall", methods=['GET'])
def sendTotalAppCount():
    dataset = applicationsCollection.find().count()
    return json_util.dumps(dataset)

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
        myQuery = {'_id': ObjectId(request.json['_id'])}
        myRequestWithoutId = request.json
        del myRequestWithoutId['_id']
        applicationsCollection.replace_one(myQuery, myRequestWithoutId, upsert=True)
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

    # Prepare the filter (find) object
    #########################

    findObj = {}

    # Document ID
    suppliedId = request.args.get("id")
    if suppliedId is not None:
        findObj["_id"] = ObjectId(suppliedId)

    # Featured
    isFeatured = request.args.get("featured")
    if isFeatured is not None:
        findObj["isFeatured"] = request.args.get("featured") == "true"

    # Support Status
    supportStatus = request.args.get("supportStatus")
    if supportStatus is not None:
        parsedStatuses = supportStatus.split(',')
        findObj["supportStatus"] = {"$in": parsedStatuses}

    # Title
    suppliedTitle = request.args.get("title")
    if suppliedTitle is not None:
        findObj["title"] = {"$regex": suppliedTitle}

    # Utilized Skills
    keywords = request.args.get("keywords")
    if keywords is not None:
        parsedKeywords = keywords.split(',')
        findObj["keywords"] = {"$in": parsedKeywords}
    
    # Deployment Status
    isDeployed = request.args.get("deployed")
    if isDeployed is not None:
        findObj["deployedLink"] = {"$ne": None}


    # Prepare the sort object
    #########################

    sortArr = []
    
    # Date
    sortDate = request.args.get("sortDate")
    if sortDate is not None:
        sortArr.append(("publishDate", pymongo.DESCENDING if request.args.get("sortDate") == "desc" else pymongo.ASCENDING))

    # Default
    if not sortArr: # Mongo query won't work if the sort array is empty, so give it something to sort on
        sortArr.append(("isFeatured", pymongo.DESCENDING))
        sortArr.append(("publishDate", pymongo.DESCENDING))

    # Prepare the limit and skip values
    #########################
    
    # Skip
    providedSkip = request.args.get("skip")
    skipValue = 0
    if providedSkip is not None:
        skipValue = int(providedSkip)

    #Limit
    providedLimit = request.args.get("limit")
    limitValue = 0
    if providedLimit is not None:
        limitValue = int(providedLimit)

    # Make the DB Query
    #########################

    dataset = applicationsCollection.find(findObj).sort(sortArr).skip(skipValue).limit(limitValue)
    return jsonResponse(dataset)
