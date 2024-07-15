# General imports

# MongoDB specific imports

# File Imports
from apis.utils.common import *

# Define collections
skills_collection = database["skills"]

# Define blueprint
Skills = Blueprint('Skills', __name__)


# Begin routes

@Skills.route("/api/skills", methods=['GET'])
def process_skills_read():
    if request.method == 'GET':
        dataset = skills_collection.find().sort([("type", pymongo.ASCENDING), ("name", pymongo.ASCENDING)])
        return json_response(flatten_mongo_ids(dataset))


@Skills.route("/api/skills", methods=['POST', 'PUT', 'DELETE'])
def process_skills_write():
    # For write actions, authenticate the user
    if not is_authenticated_user(request):
        return handle_unauthenticated_request()

    if request.method == 'POST':

        try:
            my_request = request.json
            my_request['is_proficient'] = True if (request.json['is_proficient'] == 'true' or request.json[
                'is_proficient'] == True) else False  # Parse bool
            my_request['is_visible_in_app_details'] = True if (
                        request.json['is_visible_in_app_details'] == 'true' or request.json[
                    'is_visible_in_app_details'] == True) else False  # Parse bool

            skills_collection.insert_one(my_request)
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
            my_request_without_id['is_proficient'] = True if (request.json['is_proficient'] == 'true' or request.json[
                'is_proficient'] == True) else False  #Parse bool
            my_request_without_id['is_visible_in_app_details'] = True if (
                        request.json['is_visible_in_app_details'] == 'true' or request.json[
                    'is_visible_in_app_details'] == True) else False  # Parse bool
            del my_request_without_id['_id']
            del my_request_without_id['_idFlat']
            skills_collection.replace_one(my_query, my_request_without_id, upsert=True)
            return handle_successful_write_request()

        # If data doesn't conform to validations, return error
        except Exception as e:
            print(e)
            return Response(status=415)

    if request.method == 'DELETE':
        skills_collection.delete_one({'_id': ObjectId(request.json['_id'])})
        return handle_successful_write_request()


@Skills.route("/api/skills/one", methods=['GET'])
def send_filtered_keywords():
    # Initialize the find object
    find_obj = {}

    # Document ID
    supplied_id = request.args.get("id")
    if supplied_id is not None:
        find_obj["_id"] = ObjectId(supplied_id)

    # Skill Code
    supplied_code = request.args.get("skillCode")
    if supplied_code is not None:
        find_obj["code"] = supplied_code

    # Demonstrable
    is_demonstrable = request.args.get("demonstrable")
    if is_demonstrable is not None:
        find_obj["showOnPortfolio"] = request.args.get("demonstrable") == "true"

    # Proficient
    is_proficient = request.args.get("proficient")
    if is_proficient is not None:
        find_obj["showInGallery"] = request.args.get("proficient") == "true"

    # Initialize the sort array
    sort_arr = []

    # Name
    sort_name = request.args.get("sortName")
    if sort_name is not None:
        sort_arr.append(("name", pymongo.ASCENDING if request.args.get("sortName") == "asc" else pymongo.DESCENDING))

    # Type
    sort_type = request.args.get("sortType")
    if sort_type is not None:
        sort_arr.append(("type", pymongo.ASCENDING if request.args.get("sortName") == "asc" else pymongo.DESCENDING))

    # Default
    if not sort_arr:  # Mongo query won't work if the sort array is empty, so give it something to sort on
        sort_arr.append(("name", pymongo.ASCENDING))

    # Make the DB Query
    dataset = skills_collection.find(find_obj).sort(sort_arr)
    return json_response(flatten_mongo_ids(dataset))
