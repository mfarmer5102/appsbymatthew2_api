# General imports

# MongoDB specific imports

# File Imports
from apis.utils.common import *

# Define collections
supportStatusesCollection = database["support_statuses"]

# Define blueprint
SupportStatuses = Blueprint('SupportStatuses', __name__)


# Begin routes

@SupportStatuses.route("/api/supportStatuses", methods=['GET'])
def processSkillsRead():
    if request.method == 'GET':
        dataset = supportStatusesCollection.find().sort([("label", pymongo.ASCENDING), ("code", pymongo.ASCENDING)])
        return jsonResponse(flattenMongoIds(dataset))
