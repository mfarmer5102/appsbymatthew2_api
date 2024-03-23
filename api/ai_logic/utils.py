import json
from json import dumps


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
    x = function_name
    if x == 'create_upsert_statement':
        print(function_name, function_output)
    elif x == 'extract_application_info':
        print(function_name, function_output)
    elif x == 'extract_skill_info':
        print(function_name, function_output)
    else:
        print('Function name not found.')
