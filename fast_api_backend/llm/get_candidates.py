import openai
import json
import os
from dotenv import load_dotenv

load_dotenv(".env")
QA_PROMPT = """Based on the chat history given below
{chat_summary}
You need to fill in the JSON object given below,Keep a key empty if nothing can be extracted for a particular key
{{
    "budget":"",
    "required skills":[],
    "role type": ""
    "message": ""
}}

Information about the keys:-
budget = The amount the client is willing to pay, It should be in USD and only a numeric value without $ sign
required skills = list of skills client is looking for in a candidate
role type = Wether the client is looking for full time or part time candidate, It should be one of the following values 'Full Time', 'Part Time', 'Both Full Time And Part Time'
message = If data for any of the above key, You should write a message asking for those key information, Else just write the required results are being displayed

If some fields are not mentioned, You need to keep them empty and ask user to enter those fields through message in "message" field
JSON Respone:"""

openai.api_key = os.environ.get("OPENAI_API_KEY")


def get_response(chat_history):
    print(chat_history)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": QA_PROMPT.format(chat_summary=str(chat_history)),
            }
        ],
    )
    print("RESPONSE", completion.choices[0].message)
    return json.loads(completion.choices[0].message.content)
