import os
import json
import pickle

def get_flat_json_files(path):
    data = []
    if os.path.isdir(path):
        print(path, "is dir")
        for filename in os.listdir(path):
            print(data, path, filename)
            data += get_flat_json_files(os.path.join(path, filename))
    elif path.endswith(".json"):
        with open(path) as f:
            data.append((os.path.split(path)[-1][:-5], json.load(f)))  
    
    return data
 

def pkl_dump(parent_dir, session_id, game_state):
    with open(os.path.join(parent_dir, f"{session_id}.pkl"), "wb") as f:
        pickle.dump(game_state, f)

def pkl_load(parent_dir, session_id):
    with open(os.path.join(parent_dir, f"{session_id}.pkl"), "rb") as f:
        return pickle.load(f)