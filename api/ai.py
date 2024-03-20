import os
from openai import OpenAI
from common import *
from bson.json_util import dumps

# Define blueprint
Ai = Blueprint('Ai', __name__)


# Begin routes

@Ai.route("/api/ai/generateEmbeddings", methods=['GET'])
def generate_embedding():
    if request.method == 'GET':
        user_input = request.args.get("text")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Embed a line of text
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[user_input]
        )
        # Extract the AI output embedding as a list of floats
        embedding = response.data[0].embedding
        return embedding


@Ai.route("/api/ai/searchEmbeddings", methods=['GET'])
def search_embedding():
    if request.method == 'GET':
        user_input = request.args.get("text")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Embed a line of text
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[user_input]
        )
        # Extract the AI output embedding as a list of floats
        embedding = response.data[0].embedding

        applicationsCollection = database["applications"]

        cursor = applicationsCollection.aggregate(
            [
                {
                    "$vectorSearch":
                        {
                            "index": "vector_index",
                            "path": "embeddings",
                            "queryVector": embedding,
                            "limit": 5,
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

@Ai.route("/api/ai/searchEmbeddingsPlus", methods=['GET'])
def search_embedding_plus():
    if request.method == 'GET':
        user_input = request.args.get("text")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Embed a line of text
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[user_input]
        )
        # Extract the AI output embedding as a list of floats
        embedding = response.data[0].embedding
        # print(embedding)

        applicationsCollection = database["applications"]

        cursor = applicationsCollection.aggregate(
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

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                    You are a friendly, playful Golden Retriever.
                    You explains information about Matt's portfolio to potential employers in a heavily dog-like way.
                    Your goal is to hype Matt up and help him get a job.
                    You will only receive a few records and never the full dataset.
                """},
                {"role": "system", "content": json_data},
                {"role": "user", "content": user_input}
            ]
        )

        elaboration = completion.choices[0].message.content

        return {"text": elaboration}

@Ai.route("/api/ai/defineMongoFilter", methods=['GET'])
def generate_mongo_filter():
    if request.method == 'GET':
        user_input = request.args.get("text")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": """
                    You return and only return Mongo queries. 
                    Do not prefix or suffix answers with additional text.
                    I have a Mongo database with the following collections: applications, skills. 
                    The skills collection contains information on technical skills and has the following fields: name, code, is_featured, and skill_type_code. 
                    The applications collection contains information on applications and has the following fields: title, is_featured, description, and associated_skill_codes. 
                    The associated_skill_codes field is an array that contains elements corresponding to the code field of the skills collection. 
                    Items in associated_skill_types are skill names stored in uppercase with no spaces.
                    Never use abbreviations and always use uppercase when filtering on skill codes.
                    By default on the applications collection, sort by is_featured descending and publish_date descending.
                    Given this, generate Mongo queries to return data relevant to use requests.
                """},
                {"role": "user", "content": user_input}
            ]
        )

        return {
            "text": completion.choices[0].message.content
        }


@Ai.route("/api/ai/functionCalls", methods=['GET'])
def do_function_calls():

    if request.method == 'GET':

        user_input = request.args.get("text")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        prompt = f""" Please extract information from the following and return it as a JSON object: {user_input}"""

        student_custom_functions = [
            {
                'name': 'extract_application_info',
                'description': """
                    Get the application information from the body of the input text.
                """,
                'parameters': {
                    'type': 'object',
                    # "required": [
                    #     "title",
                    #     "is_featured"
                    # ],
                    'properties': {
                        'title': {
                            'type': 'string',
                            'description': 'Name of the application'
                        },
                        'publish_date': {
                            'type': 'string',
                            'description': 'The date on which the application was published'
                        },
                        'description': {
                            'type': 'string',
                            'description': 'A description for the application, or how the application is described.'
                        },
                        'image_url': {
                            'type': 'string',
                            'description': 'The image or thumbnail to show for the application.'
                        },
                        'deployed_link': {
                            'type': 'string',
                            'description': 'The URL or link at which the application is deployed.'
                        },
                        'is_featured': {
                            'type': 'boolean',
                            'description': 'Whether or not the application is featured.',
                            "default": False
                        },
                        'support_status': {
                            'type': 'string',
                            'description': 'The current support status of the application.',
                            'enum': [
                                'ACTIVE',
                                'DISCONTINUED',
                                'EXPERIMENTAL',
                                'INACTIVE'
                            ],
                            "default": "ACTIVE"
                        },
                        'associated_skills': {
                            'type': 'array',
                            'description': 'A list of technical skills demonstrated by, used by, or associated with the application.',
                            'items': {
                                'type': 'string',
                                'enum': [
                                    'React',
                                    'GraphQL',
                                    'Python'
                                ]
                            }
                        }
                    }
                }
            }
        ]

        # Generating response back from gpt-3.5-turbo
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            functions=student_custom_functions,
            function_call='auto'
        )

        x = json.loads(response.choices[0].message.function_call.arguments)

        try:
            x['title'] = x['title'].title()
        except:
            print("couldn't apply title casing to title")

        print(x)

        return {"text": x}
