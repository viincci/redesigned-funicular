from flask import Flask, request, jsonify
import traceback
import random
import openai
import json
import os

os.environ['api_key'] = "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"
os.environ['company_discription'] = ''
os.environ['ceo_profile'] = ''
os.environ['prompt_b'] = ''

openai.api_key = os.environ.get("api_key")

app = Flask(__name__)

class Query:
    def __init__(self, query_result):
        self.queryText = query_result['queryText']

@app.route('/')
def home():
    return "Hello World"

@app.route('/webhook', methods=['POST'])
def webhook():
    witty_responses = [
        "Oops, I must have missed that. Let me try again.",
        "Don't worry, I'll figure it out. I'm an AI after all.",
        "I don't make mistakes, I have unexpected learning opportunities.",
        "Give me a minute let me think about it.",
        "Slow down your talking to fast, try again but slower this time"
    ]
    try:
        data = request.get_json()
        query = Query(data['queryResult'])
        user_input = query.queryText.lower()+"?"
        prompt_b = os.environ.get("prompt_b")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{prompt_b + user_input}",
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=["Human:", " AI:"]
        )
        response = json.dumps(response)
        res = json.loads(response)
        output = res["choices"][0]["text"]
        return jsonify({'fulfillmentText': str(output).replace("AI:"," ")})
    except:
        print(traceback.format_exc())
        return jsonify({'fulfillmentText': random.choice(witty_responses)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)

