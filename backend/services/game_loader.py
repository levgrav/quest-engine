import os
import json
from ..utils.file_ops import get_flat_json_files, unflatten_json_files

GAME_TEMPLATE_DIR = "backend/game_data/game_templates"
TEMPLATE_FILE_DIR = "backend/game_data/template_files"

def list_templates():
    return [f for f in os.listdir(GAME_TEMPLATE_DIR) if os.path.isdir(os.path.join(GAME_TEMPLATE_DIR, f))]

def load_template(template_name: str):
    path = os.path.join(GAME_TEMPLATE_DIR, template_name)
    game_data = get_flat_json_files(path)
    return game_data

def load_default_template():
    path = os.path.join(TEMPLATE_FILE_DIR, "game.json")
    with open(path, "r") as f:
        return json.load(f)

def save_template(template_name: str, data: dict):
    path = os.path.join(GAME_TEMPLATE_DIR, template_name)
    unflatten_json_files(path, data)
    
