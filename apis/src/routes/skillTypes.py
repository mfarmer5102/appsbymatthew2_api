# General imports

# MongoDB specific imports

# File Imports
from apis.utils.common import *

# Define collections
skillTypesCollection = database["skill_types"]

# Define blueprint
SkillTypes = Blueprint('SkillTypes', __name__)


# Begin routes

@SkillTypes.route("/api/skillTypes", methods=['GET'])
def process_skills_read():
    if request.method == 'GET':
        dataset = skillTypesCollection.find().sort([("label", pymongo.ASCENDING), ("code", pymongo.ASCENDING)])
        return jsonResponse(flattenMongoIds(dataset))
