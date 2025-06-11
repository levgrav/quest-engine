import uuid
import os
from .game_generator import generate_game
from .game_loader import load_template
from .ai import generate_response
from ..utils.file_ops import pkl_dump, pkl_load


INSTANCE_DIR = "backend/game_data/game_instances"

def list_instances():
    instances = [f[:-4] for f in os.listdir(INSTANCE_DIR) if f.endswith(".pkl")]
    instance_data = [get_instance_data(i, "name", "last_modified") for i in instances]
    return [(i, data.get("name"), data.get("last_modified")) for i, data in zip(instances, instance_data)]

def get_instance_data(session_id, *args):
    game_state = pkl_load(INSTANCE_DIR, session_id)
    data = {arg: game_state.__getattribute__(arg) for arg in args}
    return data

def new_game(template_name: str):
    game_data = load_template(template_name)
    session_id = uuid.uuid4()
    game_state = generate_game(game_data)
    pkl_dump(INSTANCE_DIR, session_id, game_state)
    return session_id

def load_instance(session_id: str):
    return pkl_load(INSTANCE_DIR, session_id)

def update_game(session_id: str, action: str):
    game_state = pkl_load(INSTANCE_DIR, session_id)
    game_state.add_message(action)
    response = generate_response(game_state)
    game_state.add_message(response)
    print(game_state.display_messages)
    game_state.set_last_modified()
    pkl_dump(INSTANCE_DIR, session_id, game_state)
    return game_state

def get_messages(session_id: str):
    game_state = pkl_load(INSTANCE_DIR, session_id)
    return game_state.messages