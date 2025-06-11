from fastapi import APIRouter
from ..schemas.game import StartRequest, ActionRequest
from ..services import game_loader, game_runner

router = APIRouter()

@router.get("/list_templates")
def list_templates():
    return game_loader.list_templates()

@router.get("/list_instances")
def list_instances():
    return game_runner.list_instances()

@router.post("/new_game")
def new_game(req: StartRequest):
    session_id = game_runner.new_game(req.template)
    return {"session_id": session_id}

@router.post("/action")
def do_action(req: ActionRequest):
    new_state = game_runner.update_game(req.session_id, req.command)
    return new_state

@router.get("/state/{session_id}")
def get_state(session_id: str):
    return game_runner.load_instance(session_id)