# General imports

# MongoDB specific imports

# File Imports
from apis.utils.common import *

# Define collections
trafficReportsCollection = database["traffic_reports"]

# Define blueprint
TrafficReports = Blueprint('TrafficReports', __name__)


# Begin routes

@TrafficReports.route("/api/trafficReports", methods=['GET'])
def process_traffic_reports_read():
    # User must be admin to pull any info
    if not isAuthenticatedUser(request):
        return handleUnauthenticatedRequest()

    if request.method == 'GET':
        dataset = trafficReportsCollection.find().sort([("report_end_date", pymongo.DESCENDING)])
        return jsonResponse(flattenMongoIds(dataset))
