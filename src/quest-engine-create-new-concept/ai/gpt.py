import openai
import json
import os
from ai.gpt_functions import Gpt_Functions
from openai import APIConnectionError

class Gpt:
    def __init__(self, app) -> None:

        self.app = app
        self.functions = Gpt_Functions(app)

        if os.path.exists("openai_api_key.txt"):
            with open("openai_api_key.txt") as f:
                self.key = f.readline().strip()
        else:
            with open("openai_api_key.txt", "w") as f:
                f.write("[Please enter your OpenAI API key here]")
                self.key = "[Please enter your OpenAI API key here]"


        with open(r"src\quest-engine-create\ai\system_message.txt") as f:
            self.system_message = f.read()

        self.system_message = ""


        self.messages = [
            {"role": "system", "content": self.system_message}
        ]

        # --- Variables --- #
        # Define the function in the format expected by the OpenAI API
        with open(r"src\quest-engine-create-new-concept\ai\tools.json") as f:
            self.tools = json.load(f)

        # Connection Test:
        done = False
        while not done:
            try:
                self.client = openai.OpenAI(api_key=self.key)
                self.get_response()
                done = True
            except APIConnectionError as e:
                self.app.log.log(str(e))
                self.app.log.log("Failed to connect to OpenAI API. Please check your API key in 'openai_api_key.txt'.")
                print(str(e))
                self.key = input("Failed to connect to OpenAI API. Please check your API key in 'openai_api_key.txt' or enter a valid key here. To find or make and API key got to https://platform.openai.com/api-keys. ('x' to quit)\n")
                if self.key == "x":
                    done = True

        if self.key == "x":
            self.app.log.log("OpenAI API key not found. Please create a file called 'openai_api_key.txt' in the root directory of the project and add your OpenAI API key to it.")
            self.app.quit()
            return  
        else:
            self.app.log.log("Connected to OpenAI API.")
            with open("openai_api_key.txt", "w") as f:
                f.write(self.key)

    # --- Functions --- #
    def get_response(self):
        return self.client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=self.messages,
            response_format={
                "type": "text"
            },
            tools=self.tools,
            temperature=1,
            max_completion_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            store=False
        )

    def update_messages(self):
        self.app.log.log(json.dumps(self.messages[-1]))
        tries = 0
        response = None
        while tries < 3:
            try:
                response = self.get_response()
                break
            except Exception as e:
                tries += 1
                self.app.log.log(str(e))

        if response == None:
            self.app.log.log("Failed to get response")
            return
        
        self.messages.append(response.choices[0].message.to_dict())
        self.app.log.log(json.dumps(response.choices[0].message.to_dict()))

        if response.choices[0].finish_reason == "tool_calls":
            for call in response.choices[0].message.tool_calls:
                value = self.functions.evaluate(call.to_dict())
                message = {
                    "role": "tool",
                    "content": [
                        {
                            "type": "text",
                            "text": value
                        }
                    ],
                    "tool_call_id": call.id
                }
                self.messages.append(message)
            
            self.update_messages()