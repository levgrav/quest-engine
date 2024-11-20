from json import JSONEncoder

class QuestEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        return JSONEncoder.default(self, o)