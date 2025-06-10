from fastapi import FastAPI
from backend.routers import game, user

app = FastAPI()

app.include_router(game.router, prefix="/game")
app.include_router(user.router, prefix="/user")

# backend/routers/game.py
from fastapi import APIRouter
from backend.schemas.game import GameStartRequest, GameResponse, GameInputRequest
from backend.services.game_engine import start_game, process_input
from backend.services.save_load import save_game_state, load_game_state

router = APIRouter()

@router.post("/start", response_model=GameResponse)
def start_new_game(request: GameStartRequest):
    return start_game(request.player_name)

@router.post("/input", response_model=GameResponse)
def input_to_game(request: GameInputRequest):
    return process_input(request.player_name, request.input_text)

@router.post("/save")
def save_game(request: GameStartRequest):
    save_game_state(request.player_name)
    return {"status": "saved"}

@router.post("/load", response_model=GameResponse)
def load_game(request: GameStartRequest):
    return load_game_state(request.player_name)