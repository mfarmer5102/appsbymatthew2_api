from openai import OpenAI
from apis.src.ai_logic.function_calls.index import defined_functions
from apis.src.ai_logic.utils import execute_embedding_generation, execute_embedding_search, execute_function_call, \
    execute_chat_completion, handle_function_call
from apis.utils.common import *

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


@Ai.route("/api/ai/genericFunctionCall", methods=['GET'])
def do_generic_function_call_endpoint():
    if request.method == 'GET':

        user_input = request.args.get("text")
        x, y = execute_function_call(client, user_input, defined_functions)

        print(x, y)
        res = handle_function_call(x, y)
        print('*****', res)

        print(type(res))

        built_reply = {
            'data': res,
            'function_name': y
        }

        print(built_reply)

        return json.dumps(built_reply)
