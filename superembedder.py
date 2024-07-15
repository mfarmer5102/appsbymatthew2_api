from openai import OpenAI
from common import *
from bson.json_util import dumps

applicationsCollection = database["applications"]


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
    applicationsCollection.update_one({'title': title}, {"$set": {'embeddings': vector}}, upsert=True)


def loop_through():
    allApps = applicationsCollection.find()

    json_data = json.loads(dumps(allApps))
    for app in json_data:
        del app['_id']
        del app['publish_date']
        try:
            del app['embeddings']
        except:
            print('no embeddings to delete')
        app['associated_skill_codes'] = ', '.join(app['associated_skill_codes'])
        print(app)
        stringy = json.dumps(app, separators=(',', ':'))
        print(stringy)
        vector = generate_embedding(stringy)
        print(app['title'])
        upsert_embeddings(app['title'], vector)

    # print(generate_embedding(json_data[0]))


loop_through()
