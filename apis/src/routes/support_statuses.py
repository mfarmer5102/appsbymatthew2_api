from apis.utils.common import *
from apis.globals.mongo_coll_names import support_statuses_coll

# Define blueprint
SupportStatuses = Blueprint('SupportStatuses', __name__)


# Begin routes

@SupportStatuses.route("/api/supportStatuses", methods=['GET'])
def process_skills_read():
    if request.method == 'GET':
        dataset = support_statuses_coll.ref.find().sort([("label", pymongo.ASCENDING), ("code", pymongo.ASCENDING)])
        return json_response(flatten_mongo_ids(dataset))
