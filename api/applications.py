# General imports
from flask import Flask, Blueprint, request, jsonify
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json
import datetime

# Define database
myclient = pymongo.MongoClient(os.getenv('DB_URL', "mongodb://localhost:27017"))
database = myclient[(os.getenv('DB_NAME', "appsbymatthew_dev"))]

# Define collections
applicationsCollection = database["applications"]

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
        # Prepare the filter (find) object
        #########################

        findObj = {}

        # Application Document ID
        suppliedId = request.args.get("applicationId")
        if suppliedId is not None:
            findObj["_id"] = ObjectId(suppliedId)

        # Featured
        isFeatured = request.args.get("featured")
        if isFeatured is not None:
            findObj["is_featured"] = request.args.get("featured") == "true"

        # Support Status
        supportStatusCode = request.args.get("supportStatus")
        if supportStatusCode is not None:
            findObj["support_status_code"] = supportStatusCode

        # Title
        suppliedTitle = request.args.get("title")
        if suppliedTitle is not None:
            findObj["title"] = {"$regex": suppliedTitle, '$options' : 'i'}

        # Utilized Skills
        skills = request.args.get("skills")
        if skills is not None:
            parsedSkillCodes = skills.split(',')
            findObj["associated_skill_codes"] = {"$in": parsedSkillCodes}
        
        # Deployment Status
        isDeployed = request.args.get("deployed")
        if isDeployed is not None:
            findObj["deployed_link"] = {"$ne": None}


        # Prepare the sort object
        #########################

        sortArr = []
        
        # Date
        sortDate = request.args.get("sortDate")
        if sortDate is not None:
            sortArr.append(("publish_date", pymongo.DESCENDING if request.args.get("sortDate") == "desc" else pymongo.ASCENDING))

        # Default
        if not sortArr: # Mongo query won't work if the sort array is empty, so give it something to sort on
            sortArr.append(("is_featured", pymongo.DESCENDING))
            sortArr.append(("publish_date", pymongo.DESCENDING))

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

        print(findObj)
        dataset = applicationsCollection.find(findObj).sort(sortArr).skip(skipValue).limit(limitValue)
        x = jsonResponse(dataset)
        return x

    if request.method == 'POST':
        print(request.json)
        x = request.json
        x['publish_date'] = datetime.datetime.strptime(request.json['publish_date'], '%Y-%m-%d')
        x['is_featured'] = True if request.json['is_featured'] == 'true' else False
        applicationsCollection.insert_one(x)
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
        myRequestWithoutId['publish_date'] = datetime.datetime.strptime(request.json['publish_date'], '%Y-%m-%d')
        print(myRequestWithoutId)
        # myRequestWithoutId['is_proficient'] = True if request.json['is_proficient'] == 'true' else False
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
