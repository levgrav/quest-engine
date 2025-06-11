import os
from ..utils.file_ops import get_flat_json_files

TEMPLATE_DIR = "backend/game_data/game_templates"

def list_templates():
    return [f for f in os.listdir(TEMPLATE_DIR) if os.path.isdir(os.path.join(TEMPLATE_DIR, f))]

def load_template(template_name: str):
    path = os.path.join(TEMPLATE_DIR, template_name)
    game_data = get_flat_json_files(path)
    return game_data

