import uuid

class GameObject:
    def __init__(self, name, id = None, tags = [], relations = [], properties = [], **kwargs):
        self.name = name
        self.id = id if id != None else uuid.uuid4()
        self.tags = tags
        self.relations = relations
        self.properties = properties

        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def update(self, **data):
        for key, value in data.items():
            self.__setattr__(key, value)

    def __str__(self):
        return (f"GameObject({", ".join([f"{key} = {value}" for key, value in self.__dict__.items()])})")

from datetime import datetime
from .functions import PlayFunctions

class MatchingIDsError(Exception):
    def __init__(self, id, *args):
        super().__init__(f"one or more GameObjects has the id '{id}'", *args)

class GameWorld:
    def __init__(self, game_objects = {}, **kwargs):
        
        self.game_objects = game_objects
        self.last_modified = datetime.now()
        self.clear_log()
        self.display_messages = []
        self.assert_unique_ids()

        for key, value in kwargs.items():
            self.__setattr__(key, value)

        self.gpt_data = {'type': 'play',
            'key_path': 'openai_api_key.txt',
            'tools_path': 'backend/models/play_tools.json',
            'sm_path': 'backend/models/play_system_message.txt'
        }

    def assert_unique_ids(self):
        ids = []
        for o in self.game_objects.values():
            if o.id in ids:
                raise MatchingIDsError(o.id)
            else:
                ids.append(o.id)

    def log(self, message):
        self._log.append(message)
        with open("backend/models/log.txt", 'a') as f:
            f.write(message + '\n')

    def get_log(self):
        return self._log
    
    def clear_log(self):
        with open("backend/models/log.txt", 'w') as f:
            f.write('')
        self._log = []

    def set_last_modified(self):
        self.last_modified = datetime.now()

    def process_action(self, action, gpt):
        self.display_messages.append(f"[Player]: {action}")
        gpt.messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": action
                }
            ]
        })
        gpt.update_messages()
        self.display_messages.append(f"[Game]: {gpt.messages[-1]['content']}")
        self.gpt_data.update(gpt.get_data())

    def __str__(self):
        return (f"GameObject({", ".join([f"{key} = {value}" for key, value in self.__dict__.items()])})")