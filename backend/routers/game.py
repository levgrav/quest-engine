from fastapi import APIRouter
from ..schemas.game import StartRequest, ActionRequest
from ..services import game_loader, game_runner
from ..utils.logger import log

router = APIRouter()

@router.get("/list_templates")
def list_templates():
    log(f'@router.get("/list_templates")')
    return game_loader.list_templates()

@router.get("/list_instances")
def list_instances():
    log(f'@router.get("/list_instances")')
    return game_runner.list_instances()

@router.post("/new_game")
def new_game(req: StartRequest):
    log(f'@router.post("/new_game")')
    session_id = game_runner.new_game(req.template)
    return {"session_id": session_id}

@router.post("/action")
def do_action(req: ActionRequest):
    log(f'@router.post("/action")')
    new_state = game_runner.update_game(req.session_id, req.command)
    return new_state

@router.get("/state/{session_id}")
def get_state(session_id: str):
    log(f'@router.get("/state/{session_id}")')
    return game_runner.load_instance(session_id)

@router.get("/template/{template_name}")
def get_template(template_name: str):
    log(f'@router.get("/template/{template_name}")')
    if template_name == "new":
        return game_loader.load_default_template()
    return game_loader.load_template(template_name)

@router.post("/template/{template_name}")
def save_template(template_name: str, data: dict = {}):
    log(f'@router.post("/template/{template_name}")')
    return game_loader.save_template(template_name, data)