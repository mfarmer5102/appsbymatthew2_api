from apis.utils.common import database

skills_collection = database["skills"]


def resolve_find_one_skill_statement(func_output):
    try:
        print(func_output['find_clause'])
        res = skills_collection.find_one(
            func_output['find_clause'],
            {'_id': 0}
        )
        print(res)
        return res
    except Exception as error:
        print(error)
        return "Sorry, I encountered an issue while trying to find that skill."


def resolve_find_many_skill_statement(func_output):
    try:
        res = skills_collection.find(
            func_output['find_clause'],
            {'_id': 0}
        ).limit(1000)
        print(res)
        res_arr = []
        for app in res:
            res_arr.append(app)
        print(res_arr)
        return res_arr
    except Exception as error:
        print(error)
        return "Sorry, I encountered an issue while trying to find those skills."
