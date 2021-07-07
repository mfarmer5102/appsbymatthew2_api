# General imports
from flask import Flask, Blueprint, request, jsonify

# MongoDB specific imports
import pymongo
from bson import json_util, ObjectId
import json

# File Imports
from common import *

# Define collections
skillsCollection = database["skills"]

# Define blueprint
Skills = Blueprint('Skills', __name__)

# Begin routes

@Skills.route("/api/skills", methods=['GET'])
def processSkillsRead():

    if request.method == 'GET':
        dataset = skillsCollection.find().sort([("type", pymongo.ASCENDING), ("name", pymongo.ASCENDING)])
        return jsonResponse(flattenMongoIds(dataset))

@Skills.route("/api/skills", methods=['POST', 'PUT', 'DELETE'])
def processSkillsWrite():

    # For write actions, authenticate the user
    if not isAuthenticatedUser(request): 
        return handleUnauthenticatedRequest()

    if request.method == 'POST':

        try:
            myRequest = request.json
            myRequest['is_proficient'] = True if (request.json['is_proficient'] == 'true' or request.json['is_proficient'] == True) else False # Parse bool
            myRequest['is_visible_in_app_details'] = True if (request.json['is_visible_in_app_details'] == 'true' or request.json['is_visible_in_app_details'] == True) else False # Parse bool

            skillsCollection.insert_one(myRequest)
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
            myRequestWithoutId['is_proficient'] = True if (request.json['is_proficient'] == 'true' or request.json['is_proficient'] == True) else False #Parse bool
            myRequestWithoutId['is_visible_in_app_details'] = True if (request.json['is_visible_in_app_details'] == 'true' or request.json['is_visible_in_app_details'] == True) else False # Parse bool
            del myRequestWithoutId['_id']
            skillsCollection.replace_one(myQuery, myRequestWithoutId, upsert=True)
            return handleSuccessfulWriteRequest()

        # If data doesn't conform to validations, return error
        except Exception as e:
            print(e)
            return Response(status = 415)

    if request.method == 'DELETE':

        skillsCollection.delete_one({'_id': ObjectId(request.json['_id'])})
        return handleSuccessfulWriteRequest()

@Skills.route("/api/skills/one", methods=['GET'])
def sendFilteredKeywords():

    # Initialize the find object
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

    # Initialize the sort array
    sortArr = []
    
    # Name
    sortName = request.args.get("sortName")
    if sortName is not None:
        sortArr.append(("name", pymongo.ASCENDING if request.args.get("sortName") == "asc" else pymongo.DESCENDING))

    # Type
    sortType = request.args.get("sortType")
    if sortType is not None:
        sortArr.append(("type", pymongo.ASCENDING if request.args.get("sortName") == "asc" else pymongo.DESCENDING))
    
    # Default
    if not sortArr: # Mongo query won't work if the sort array is empty, so give it something to sort on
        sortArr.append(("name", pymongo.ASCENDING))

    # Make the DB Query
    dataset = skillsCollection.find(findObj).sort(sortArr)
    return jsonResponse(flattenMongoIds(dataset))
