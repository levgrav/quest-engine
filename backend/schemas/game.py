from pydantic import BaseModel

class GameStartRequest(BaseModel):
    player_name: str

class GameInputRequest(BaseModel):
    player_name: str
    input_text: str

class GameResponse(BaseModel):
    message: str
    player_location: str