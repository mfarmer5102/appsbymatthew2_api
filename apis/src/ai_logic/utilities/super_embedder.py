from openai import OpenAI
from apis.utils.common import *
from bson.json_util import dumps

applications_collection = database["applications"]


def generate_embedding(user_input):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Embed a line of text
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=user_input
    )
    # Extract the AI output embedding as a list of floats
    embedding = response.data[0].embedding
    return embedding


def upsert_embeddings(title, vector):
    applications_collection.update_one({'title': title}, {"$set": {'embeddings': vector}}, upsert=True)


def loop_through():
    all_apps = applications_collection.find()

    json_data = json.loads(dumps(all_apps))
    for app in json_data:
        del app['_id']
        del app['publish_date']
        try:
            del app['embeddings']
        except:
            print('No embeddings to delete')
        app['associated_skill_codes'] = ', '.join(app['associated_skill_codes'])
        stringy = json.dumps(app, separators=(',', ':'))
        vector = generate_embedding(stringy)
        upsert_embeddings(app['title'], vector)

loop_through()
