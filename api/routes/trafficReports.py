# General imports
from flask import Flask, Blueprint, request, jsonify

# MongoDB specific imports
import pymongo

# File Imports
from common import *

# Define collections
trafficReportsCollection = database["traffic_reports"]

# Define blueprint
TrafficReports = Blueprint('TrafficReports', __name__)

# Begin routes

@TrafficReports.route("/api/trafficReports", methods=['GET'])
def processTrafficReportsRead():

    # User must be admin to pull any info
    if not isAuthenticatedUser(request): 
        return handleUnauthenticatedRequest()

    if request.method == 'GET':
        dataset = trafficReportsCollection.find().sort([("report_end_date", pymongo.DESCENDING)])
        return jsonResponse(flattenMongoIds(dataset))
