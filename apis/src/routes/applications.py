import datetime
import pymongo
from bson import ObjectId
from flask import request, Blueprint, Response
from apis.utils.common import *
from apis.globals.mongo_coll_names import applications_coll

# Define blueprint
Applications = Blueprint('Applications', __name__)


@Applications.route("/api/applications/countall", methods=['GET'])
def send_total_app_count():
    dataset = applications_coll.ref.find().count()
    return json_util.dumps(dataset)


@Applications.route("/api/applications", methods=['GET'])
def process_applications_read():
    if request.method == 'GET':

        # Initialize the find object
        find_obj = {}

        # Application Document ID
        supplied_id = request.args.get("applicationId")
        if supplied_id is not None:
            find_obj["_id"] = ObjectId(supplied_id)

        # Featured
        is_featured = request.args.get("featured")
        if is_featured is not None:
            find_obj["is_featured"] = request.args.get("featured") == "true"

        # Support Status
        support_status_code = request.args.get("supportStatus")
        if support_status_code is not None:
            find_obj["support_status_code"] = support_status_code

        # Title
        supplied_title = request.args.get("title")
        if supplied_title is not None:
            find_obj["title"] = {"$regex": supplied_title, '$options': 'i'}

        # Utilized Skills
        skills = request.args.get("skills")
        if skills is not None:
            parsed_skill_codes = skills.split(',')
            find_obj["associated_skill_codes"] = {"$in": parsed_skill_codes}

        # Deployment Status
        is_deployed = request.args.get("deployed")
        if is_deployed is not None:
            find_obj["deployed_link"] = {"$ne": None}

        # Initialize the sort array
        sort_arr = []

        # Date
        sort_date = request.args.get("sortDate")
        if sort_date is not None:
            sort_arr.append(
                ("publish_date", pymongo.DESCENDING if request.args.get("sortDate") == "desc" else pymongo.ASCENDING))

        # Default
        if not sort_arr:  # Mongo query won't work if the sort array is empty, so give it something to sort on
            sort_arr.append(("is_featured", pymongo.DESCENDING))
            sort_arr.append(("publish_date", pymongo.DESCENDING))

        # Skip
        provided_skip = request.args.get("skip")
        skip_value = 0
        if provided_skip is not None:
            skip_value = int(provided_skip)

        #Limit
        provided_limit = request.args.get("limit")
        limit_value = 0
        if provided_limit is not None:
            limit_value = int(provided_limit)

        # Make the DB Query
        dataset = applications_coll.ref \
            .find(find_obj, {"embeddings": 0}) \
            .sort(sort_arr).skip(skip_value) \
            .limit(limit_value)

        return json_response(flatten_mongo_ids(dataset))


@Applications.route("/api/applications", methods=['POST', 'PUT', 'DELETE'])
def process_applications_write():
    # For write actions, authenticate the user
    if not is_authenticated_user(request):
        return handle_unauthenticated_request()

    if request.method == 'POST':

        x = request.json

        try:
            x['publish_date'] = datetime.datetime.strptime(request.json['publish_date'], '%Y-%m-%d')
            x['is_featured'] = True if (request.json['is_featured'] == 'true' or request.json[
                'is_featured'] == True) else False  # Parse bool
            applications_coll.ref.insert_one(x)
            return handle_successful_write_request()

        # If data doesn't conform to validations, return error
        except Exception as e:
            print(e)
            return Response(status=415)

    if request.method == 'PUT':

        try:
            incoming_id = request.json['_id']
            my_query = {'_id': ObjectId(incoming_id['$oid'])}
            my_request_without_id = request.json
            my_request_without_id['publish_date'] = datetime.datetime.strptime(request.json['publish_date'], '%Y-%m-%d')
            my_request_without_id['is_featured'] = True if (request.json['is_featured'] == 'true' or request.json[
                'is_featured'] == True) else False  # Parse bool
            del my_request_without_id['_id']
            del my_request_without_id['_idFlat']
            applications_coll.ref.replace_one(my_query, my_request_without_id, upsert=True)
            return handle_successful_write_request()

        # If data doesn't conform to validations, return error
        except Exception as e:
            print(e)
            return Response(status=415)

    if request.method == 'DELETE':
        applications_coll.ref.delete_one({'_id': ObjectId(request.json['_id'])})
        return handle_successful_write_request()
