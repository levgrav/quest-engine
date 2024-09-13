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
        with open(r"src\quest-engine-create\ai\system_message.txt") as f:
            self.system_message = f.read()

        self.client = openai.OpenAI(api_key=self.key)

        self.messages = [
            {"role": "system", "content": self.system_message}
        ]  # TEMPORARY

        # --- Variables --- #
        # Define the function in the format expected by the OpenAI API
        with open(r"src\quest-engine-create\ai\tools.json") as f:
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
        )

    def update_messages(self):
        tries = 0
        while True:
            try:
                response = self.get_response()
                break
            except Exception as e:
                tries += 1
                print(e)

            if tries == 3:
                print("Failed to get response")
                return

        if response.choices[0].finish_reason == "tool_calls":
            for call in response.choices[0].message.tool_calls:

                self.messages.append(
                    {
                        "role": "assistant",
                        "content": [{"type": "text", "text": ""}],
                        "tool_calls": [
                            {
                                "id": call.id,
                                "type": call.type,
                                "function": {
                                    "name": call.function.name,
                                    "arguments": call.function.arguments,
                                },
                            }
                        ],
                    }
                )

                # Execute the function
                try:
                    result = self.functions.__getattribute__(call.function.name)(
                        **json.loads(call.function.arguments)
                    )
                except Exception as e:
                    result = f"Error: {e}"
                print(f"Function: {call.function.name}, Result: {result}")

                # Send the result back to the model
                self.messages.append(
                    {
                        "role": "tool",
                        "content": [{"type": "text", "text": result}],
                        "tool_call_id": call.id,
                    }
                )

            self.update_messages()
        else:
            self.messages.append(response.choices[0].message)
            print(response.choices[0].message.content)

    def process_user_input(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        self.update_messages()
        return self.messages[-1].content
