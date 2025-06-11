from pydantic import BaseModel

class StartRequest(BaseModel):
    template: str

class ActionRequest(BaseModel):
    session_id: str
    command: str