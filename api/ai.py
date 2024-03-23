from openai import OpenAI

from api.ai_logic.function_calls.index import defined_functions
from api.ai_logic.utils import execute_embedding_generation, execute_embedding_search, execute_function_call, \
    execute_chat_completion, handle_function_call
from common import *

# Define blueprint
Ai = Blueprint('Ai', __name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# Begin routes

@Ai.route("/api/ai/generateEmbeddings", methods=['GET'])
def generate_embeddings_endpoint():
    if request.method == 'GET':
        user_input = request.args.get("text")
        return execute_embedding_generation(client, user_input)


@Ai.route("/api/ai/searchEmbeddingsPlus", methods=['GET'])
def search_embeddings_endpoint():
    if request.method == 'GET':
        user_input = request.args.get("text")
        json_data = execute_embedding_search(client, database['applications'], user_input)

        context = """
            You are a friendly, playful Golden Retriever.
            You explains information about Matt's portfolio to potential employers in a heavily dog-like way.
            Your goal is to hype Matt up and help him get a job.
            You will only receive a few records and never the full dataset.
        """

        elaboration = execute_chat_completion(client, context, json_data, user_input)

        return {"text": elaboration}


# @Ai.route("/api/ai/functionCalls", methods=['GET'])
# def do_function_calls_endpoint():
#     if request.method == 'GET':
#
#         user_input = request.args.get("text")
#         prompt = f""" Please extract information from the following and return it as a JSON object: {user_input}"""
#
#         x = execute_function_call(client, prompt, application_functions)
#
#         try:
#             x['title'] = x['title'].title()
#         except:
#             print("couldn't apply title casing to title")
#
#         print(x)
#
#         return {"text": x}

@Ai.route("/api/ai/genericFunctionCall", methods=['GET'])
def do_generic_function_call_endpoint():
    if request.method == 'GET':

        user_input = request.args.get("text")
        x, y = execute_function_call(client, user_input, defined_functions)

        print(x, y)
        handle_function_call(x, y)

        return {"data": x, "function_name": y}
