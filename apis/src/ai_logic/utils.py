import json

from apis.src.ai_logic.function_calls.resolvers.application import *
from apis.src.ai_logic.function_calls.resolvers.skill import *
from apis.utils.mongo_connection import database

applications_collection = database["applications"]
skills_collection = database["skills"]


def execute_embedding_generation(client, input):
    # Embed a line of text
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[input]
    )
    # Extract the AI output embedding as a list of floats
    embedding = response.data[0].embedding
    return embedding


def execute_embedding_search(client, db_and_collection, user_input):
    embedding = execute_embedding_generation(client, user_input)

    cursor = db_and_collection.aggregate(
        [
            {
                "$vectorSearch":
                    {
                        "index": "vector_index",
                        "path": "embeddings",
                        "queryVector": embedding,
                        "limit": 10,
                        "numCandidates": 100
                    }
            },
            {
                "$project": {
                    "_id": 0,
                    "publish_date": 0,
                    "embeddings": 0
                }
            }
        ]
    )

    res_arr = []
    for datum in cursor:
        res_arr.append(datum)

    json_data = json.dumps(res_arr)
    return json_data


def execute_function_call(client, prompt, functions):
    # Generating response back from gpt-3.5-turbo
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        functions=functions,
        function_call='auto'
    )

    function_name = response.choices[0].message.function_call.name
    arguments = response.choices[0].message.function_call.arguments

    return json.loads(arguments), function_name


def execute_chat_completion(client, context, system_input, user_input):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "system", "content": system_input},
            {"role": "user", "content": user_input}
        ]
    )

    return completion.choices[0].message.content


def handle_function_call(function_output, function_name):

    # Applications
    if function_name == 'find_one_application_statement':
        return resolve_find_one_application_statement(function_output)
    elif function_name == 'find_many_application_statement':
        return resolve_find_many_application_statement(function_output)
    elif function_name == 'create_application_statement':
        return resolve_create_application_statement(function_output)
    elif function_name == 'update_application_statement':
        return resolve_update_application_statement(function_output)
    elif function_name == 'delete_application_statement':
        return resolve_delete_application_statement()

    # Skills
    elif function_name == 'find_one_skill_statement':
        return resolve_find_one_skill_statement(function_output)
    elif function_name == 'find_many_skill_statement':
        return resolve_find_many_skill_statement(function_output)

    # Default
    else:
        return 'Function name not found.'
