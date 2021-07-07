# General imports
from flask import Flask, Blueprint, request, jsonify, Response
import os

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json
import datetime

# File Imports
from common import *

# Define collections
applicationsCollection = database["applications"]

# Define blueprint
Applications = Blueprint('Applications', __name__)

# Begin routes

@Applications.route("/api/applications/countall", methods=['GET'])
def sendTotalAppCount():
    dataset = applicationsCollection.find().count()
    return json_util.dumps(dataset)

@Applications.route("/api/applications", methods=['GET'])
def processApplicationsRead():

    if request.method == 'GET':

        # Initialize the find object
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


        # Initialize the sort array
        sortArr = []
        
        # Date
        sortDate = request.args.get("sortDate")
        if sortDate is not None:
            sortArr.append(("publish_date", pymongo.DESCENDING if request.args.get("sortDate") == "desc" else pymongo.ASCENDING))

        # Default
        if not sortArr: # Mongo query won't work if the sort array is empty, so give it something to sort on
            sortArr.append(("is_featured", pymongo.DESCENDING))
            sortArr.append(("publish_date", pymongo.DESCENDING))
        
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
        dataset = applicationsCollection.find(findObj).sort(sortArr).skip(skipValue).limit(limitValue)
        return jsonResponse(flattenMongoIds(dataset))

@Applications.route("/api/applications", methods=['POST', 'PUT', 'DELETE'])
def processApplicationsWrite():

    # For write actions, authenticate the user
    if not isAuthenticatedUser(request): 
        return handleUnauthenticatedRequest()

    if request.method == 'POST':

        x = request.json

        try:
            x['publish_date'] = datetime.datetime.strptime(request.json['publish_date'], '%Y-%m-%d')
            x['is_featured'] = True if (request.json['is_featured'] == 'true' or request.json['is_featured'] == True) else False # Parse bool
            applicationsCollection.insert_one(x)
            return handleSuccessfulWriteRequest()
        
        # If data doesn't conform to validations, return error
        except Exception as e:
            print(e)
            return Response(status = 415)

    if request.method == 'PUT':

        try:
            incomingId = request.json['_id']
            myQuery = {'_id': ObjectId(incomingId['$oid'])}
            myRequestWithoutId = request.json
            myRequestWithoutId['publish_date'] = datetime.datetime.strptime(request.json['publish_date'], '%Y-%m-%d')
            myRequestWithoutId['is_featured'] = True if (request.json['is_featured'] == 'true' or request.json['is_featured'] == True) else False # Parse bool
            del myRequestWithoutId['_id']
            applicationsCollection.replace_one(myQuery, myRequestWithoutId, upsert=True)
            return handleSuccessfulWriteRequest()

        # If data doesn't conform to validations, return error
        except Exception as e:
            print(e)
            return Response(status = 415)

    if request.method == 'DELETE':

        applicationsCollection.delete_one({'_id': ObjectId(request.json['_id'])})
        return handleSuccessfulWriteRequest()
