import json
from json import dumps
from common import database

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
                "$unset": "embeddings"
            }
        ]
    )

    json_data = dumps(cursor)
    return json_data


def execute_function_call(client, prompt, functions):
    # Generating response back from gpt-3.5-turbo
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}],
        functions=functions,
        function_call='auto'
    )

    function_name = response.choices[0].message.function_call.name
    arguments = response.choices[0].message.function_call.arguments

    return json.loads(arguments), function_name


def execute_chat_completion(client, context, system_input, user_input):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "system", "content": system_input},
            {"role": "user", "content": user_input}
        ]
    )

    return completion.choices[0].message.content


def handle_function_call(function_output, function_name):

    # Function name
    x = function_name
    print(x)

    # Applications
    if x == 'find_application_statement':
        try:
            print(function_output['find_clause'])
            res = applications_collection.find_one(
                function_output['find_clause'],
                {'_id': 0, 'embeddings': 0}
            )
            print(res)
            return res
        except Exception as error:
            print(error)
            return "Sorry, I encountered an issue while trying to find that application."
    elif x == 'create_application_statement':
        try:
            res = applications_collection.insert_one(
                function_output['insert_clause']
            )
            print(res)
            return "Application created successfully!"
        except Exception as error:
            print(error)
            return "Sorry, I encountered an issue while trying to create that application."
    elif x == 'update_application_statement':
        try:
            res = applications_collection.update_one(
                function_output['find_clause'],
                {'$set': function_output['set_clause']},
                upsert=True
            )
            print(res)
            return "Application updated successfully!"
        except Exception as error:
            print(error)
            return "Sorry, I encountered an issue while trying to update that application."
    elif x == 'delete_application_statement':
        res = 'No, I cannot delete applications.'
        print(res)
        return res

    # Skills
    elif x == 'find_skill_statement':
        res = skills_collection.find_one(
            function_output['find_clause']
        )
        print(res)
        return res
    else:
        res = 'Function name not found.'
        print(res)
        return res