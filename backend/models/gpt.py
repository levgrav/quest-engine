import openai
import json
import os
from openai import APIConnectionError
from copy import deepcopy
from .functions import PlayFunctions, CreateFunctions

class Gpt:
    def __init__(self, game_state, **kwargs) -> None:

        self.game_state = game_state
        self.function_type = kwargs.get('function_type', 'play')
        self.functions = PlayFunctions(game_state) if self.function_type == 'play' else CreateFunctions(game_state)

        if 'key' in kwargs:
            self.key = kwargs['key']
        else:
            key_path = kwargs.get('key_path', 'openai_api_key.txt')
            if os.path.exists(key_path):
                with open(key_path) as f:
                    self.key = f.readline().strip()
            else:
                with open(key_path, "w") as f:
                    f.write("[Please enter your OpenAI API key here]")
                    self.key = "[Please enter your OpenAI API key here]"

        if 'system_message' in kwargs:
            self.system_message = kwargs['system_message']
        else:
            sm_path = kwargs.get('sm_path', f"backend/models/{self.function_type}_system_message.txt")
            if os.path.exists(sm_path):
                with open(sm_path) as f:
                    self.system_message = f.read()
            else:
                self.system_message = ""


        self.messages = kwargs.get('messages', [
            {"role": "system", "content": self.system_message}
        ])

        if 'tools' in kwargs:
            self.tools = kwargs['tools']
        else:
            tools_path = kwargs.get('tools_path', f"backend/models/{self.function_type}_tools.txt") 
            if os.path.exists(tools_path):
                with open(tools_path) as f:
                    self.tools = json.load(f)
            else: 
                self.tools = {}

        # Connection Test:
        done = False
        while not done:
            try:
                self.client = openai.OpenAI(api_key=self.key)
                self.get_response()
                done = True
            except APIConnectionError as e:
                self.game_state.log(str(e))
                self.game_state.log("Failed to connect to OpenAI API. Please check your API key in 'openai_api_key.txt'.")
                print(str(e))
                self.key = input("Failed to connect to OpenAI API. Please check your API key in 'openai_api_key.txt' or enter a valid key here. To find or make and API key got to https://platform.openai.com/api-keys. ('x' to quit)\n")
                if self.key == "x":
                    done = True

        if self.key == "x":
            self.game_state.log("OpenAI API key not found. Please create a file called 'openai_api_key.txt' in the root directory of the project and add your OpenAI API key to it.")
            self.game_state.quit()
            return  
        else:
            self.game_state.log("Connected to OpenAI API.")
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
        self.game_state.log(json.dumps(self.messages[-1]))
        tries = 0
        response = None
        while tries < 3:
            try:
                response = self.get_response()
                break
            except Exception as e:
                tries += 1
                self.game_state.log(str(e))

        if response == None:
            self.game_state.log("Failed to get response")
            return
        
        self.messages.append(response.choices[0].message.to_dict())
        self.game_state.log(json.dumps(response.choices[0].message.to_dict()))

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

    def get_data(self):
        return {
            'messages': self.messages,
            'key': self.key,
            'system_message': self.system_message,
            'tools': self.tools,
            'function_type': self.function_type
        }
