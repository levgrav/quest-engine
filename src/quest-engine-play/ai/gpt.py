import openai
import json
import os
from ai.gpt_functions import Gpt_Functions


class Gpt:
    def __init__(self, project_model) -> None:

        self.project_model = project_model
        self.functions = Gpt_Functions(project_model)

        with open("openai_api_key.txt") as f:
            self.key = f.readline().strip()
        with open(r"src\quest-engine-play\ai\system_message.txt") as f:
            self.system_message = f.read()

        self.client = openai.OpenAI(api_key=self.key)

        self.messages = [
            {"role": "system", "content": self.system_message}
        ]

        # --- Variables --- #
        # Define the function in the format expected by the OpenAI API
        with open(r"src\quest-engine-play\ai\tools.json") as f:
            self.tools = json.load(f)

    # --- Functions --- #
    def get_response(self):
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            tools=self.tools, 
        ).to_dict()

    def update_messages(self):
        tries = 0
        response = None
        while tries < 3:
            try:
                response = self.get_response()
                break
            except Exception as e:
                tries += 1
                self.project_model.log.log(e)

        if not response:
            self.project_model.log.log("Failed to get response")
            return

        if response["choices"][0]["finish_reason"] == "tool_calls":
            for call in response["choices"][0]["message"]["tool_calls"]:

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": ""}],
                        "tool_calls": [
                            {
                                "id": call["id"],
                                "type": call["type"],
                                "function": {
                                    "name": call["function"]["name"],
                                    "arguments": call["function"]["arguments"],
                                },
                            }
                        ],
                    }
                )

                # Execute the function
                args = json.loads(call["function"]["arguments"])
                try:
                    result = self.functions.__getattribute__(call["function"]["name"])(**args)
                except Exception as e:
                    result = f"Error: {e}"
                    self.project_model.log.log(f"Error args: {args}")
                self.project_model.log.log(f"Function: {call["function"]["name"]}({", ".join([f"{key} = {val}" for key, val in args.items()])}), Result: {result}")

                # Send the result back to the model
                self.messages.append(
                    {
                        "role": "tool",
                        "content": [{"type": "text", "text": result}],
                        "tool_call_id": call["id"],
                    }
                )

            self.update_messages()
        else:
            self.messages.append(response["choices"][0]["message"])
            self.project_model.log.log(response["choices"][0]["message"]["content"])

    def process_user_input(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        self.update_messages()
        return self.messages[-1]["content"]
