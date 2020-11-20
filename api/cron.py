# General imports
from flask import Flask, Blueprint, request, jsonify
import os
import requests #For making external URL call
app = Flask(__name__)

# Define blueprint
Cron = Blueprint('Cron', __name__)

# Define Cron routes
@Cron.route("/api/ping_logger", methods=['GET', 'POST', 'PUT', 'DELETE'])
def sendKeywords():

    if request.method == 'GET':
        return requests.get('https://trafficanalyzer.azurewebsites.net/api/all').content