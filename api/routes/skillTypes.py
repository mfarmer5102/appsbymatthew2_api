# General imports
from flask import Flask, Blueprint, request, jsonify

# MongoDB specific imports
import pymongo

# File Imports
from common import *

# Define collections
skillTypesCollection = database["skill_types"]

# Define blueprint
SkillTypes = Blueprint('SkillTypes', __name__)

# Begin routes

@SkillTypes.route("/api/skillTypes", methods=['GET'])
def processSkillsRead():

    if request.method == 'GET':
        dataset = skillTypesCollection.find().sort([("label", pymongo.ASCENDING), ("code", pymongo.ASCENDING)])
        return jsonResponse(flattenMongoIds(dataset))
