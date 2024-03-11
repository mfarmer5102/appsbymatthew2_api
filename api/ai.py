import os
from openai import OpenAI
from common import *

# Define blueprint
Ai = Blueprint('Ai', __name__)

# Begin routes
@Ai.route("/api/ai", methods=['GET'])
def processApplicationsRead():

    if request.method == 'GET':

        user_input = request.args.get("text")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # response_format={ "type": "json_object" },
            stop=["\n"],  # Remove line breaks in text response
            messages=[
                {"role": "system", "content": "You are helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        return {
            "text": completion.choices[0].message.content
        }