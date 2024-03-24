from common import database

applications_collection = database["applications"]


def resolve_find_one_application_statement(func_output):
    try:
        print(func_output['find_clause'])
        res = applications_collection.find_one(
            func_output['find_clause'],
            {'_id': 0, 'embeddings': 0, 'publish_date': 0}
        )
        print(res)
        return res
    except Exception as error:
        print(error)
        return "Sorry, I encountered an issue while trying to find that application."

def resolve_find_many_application_statement(func_output):
    try:
        print(func_output['find_clause'])
        res = applications_collection.find(
            func_output['find_clause'],
            {'_id': 0, 'embeddings': 0, 'publish_date': 0}
        ).sort({'publish_date': -1}).limit(100)
        res_arr = []
        for app in res:
            res_arr.append(app)
        print(res_arr)
        return res_arr
    except Exception as error:
        print(error)
        return "Sorry, I encountered an issue while trying to find that application."

def resolve_create_application_statement(func_output):
    try:
        res = applications_collection.insert_one(
            func_output['insert_clause']
        )
        print(res)
        return "Application created successfully!"
    except Exception as error:
        print(error)
        return "Sorry, I encountered an issue while trying to create that application."

def resolve_update_application_statement(func_output):
    try:
        res = applications_collection.update_one(
            func_output['find_clause'],
            {'$set': func_output['set_clause']},
            upsert=True
        )
        print(res)
        return "Application updated successfully!"
    except Exception as error:
        print(error)
        return "Sorry, I encountered an issue while trying to update that application."

def resolve_delete_application_statement():
    res = 'No, I cannot delete applications.'
    print(res)
    return res