import os
import json
import pickle
import shutil
import stat

def get_flat_json_files(base, ext = None):
    path = os.path.join(base, ext) if ext != None else base

    if os.path.isdir(path):
        data = {}
        for filename in os.listdir(path):
            data.update(get_flat_json_files(base, os.path.join(ext, filename) if ext != None else filename))
        return data
    elif path.endswith(".json"):
        with open(path) as f:
            return {ext: json.load(f)}
 
def unflatten_json_files(path: str, game_data: dict):
    if os.path.isdir(path): 
        delete_path(path)
    
    for key, data in game_data.items():
        key_path, filename = os.path.split(key)
        dirpath = os.path.join(path, key_path)
        filepath = os.path.join(path, key)
        os.makedirs(dirpath, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

def force_remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path, onexc=force_remove_readonly)
    elif os.path.exists(path):
        os.remove(path)

def pkl_dump(parent_dir, session_id, game_state):
    with open(os.path.join(parent_dir, f"{session_id}.pkl"), "wb") as f:
        pickle.dump(game_state, f)

def pkl_load(parent_dir, session_id):
    with open(os.path.join(parent_dir, f"{session_id}.pkl"), "rb") as f:
        return pickle.load(f)
    
def is_json(text: str, return_decoded = False):
    if not isinstance(text, (str, bytes, bytearray)): return False
    
    text = text.strip()
    
    if not text: return False
    if text[0] not in {'{', '['} or text[-1] not in {'}', ']'}: return False
    
    try:
        decoded = json.loads(text)        
    except (ValueError, TypeError, json.JSONDecodeError):
        return False
    
    if return_decoded: return decoded
    else: return True