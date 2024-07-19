import pymongo
from flask import Blueprint, request

from apis.utils.common import *
from apis.globals.mongo_coll_names import skill_types_coll

# Define blueprint
SkillTypes = Blueprint('SkillTypes', __name__)


@SkillTypes.route("/api/skillTypes", methods=['GET'])
def process_skills_read():
    if request.method == 'GET':
        dataset = skill_types_coll.ref.find().sort([("label", pymongo.ASCENDING), ("code", pymongo.ASCENDING)])
        return json_response(flatten_mongo_ids(dataset))
