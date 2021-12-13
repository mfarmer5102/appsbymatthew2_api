## App engine looks for main.py

# Imports
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
import os

# Define app variable
app = Flask(__name__)

# Allow cross origin requests
CORS(app)

# Define port on which to listen
port = int(os.environ.get("PORT", 5001))

# Import route files
from api.applications import Applications
from api.cron import Cron
from api.skills import Skills
from api.skillTypes import SkillTypes
from api.supportStatuses import SupportStatuses
from api.trafficReports import TrafficReports

# Register route files
app.register_blueprint(Applications)
app.register_blueprint(Cron)
app.register_blueprint(Skills)
app.register_blueprint(SkillTypes)
app.register_blueprint(SupportStatuses)
app.register_blueprint(TrafficReports)

# Root URL Route
@app.route('/')
def home():
    return '<p>The server is listening for requests.</p>'

# Start server listening
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

