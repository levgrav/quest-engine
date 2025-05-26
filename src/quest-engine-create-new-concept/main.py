# main.py

import json
import ai.gpt as gpt
from utils.logger import Log

class App():
    def __init__(self):
        self.done = False
        self.parent_dir = r"files\game_data\game_templates"
        self.log = Log("files/logs/log.txt")
        self.log.clear_log()
        self.gpt = gpt.Gpt(self)

    def main(self):
        self.done = False

        while not self.done:
            user_input = input("> ")
            if user_input == 'x':
                self.quit()
                continue
            
            self.gpt.messages.append({
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": user_input
                }]
            })
            next_message_index = len(self.gpt.messages)
            self.gpt.update_messages()
            print("\n".join(json.dumps(message, indent=2) for message in self.gpt.messages[next_message_index:]))
        
        print("Program terminated")
    
    def quit(self):
        self.done = True

if __name__ == "__main__":
    App().main()