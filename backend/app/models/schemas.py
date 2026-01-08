"""
Pydantic схемы для API
"""
from pydantic import BaseModel
from typing import Optional, List

class MoveRequest(BaseModel):
    game_id: str
    row: int
    col: int
    chat_id: Optional[str] = None

class GameResponse(BaseModel):
    game_id: str
    board: List[List[str]]
    status: str
    winner: Optional[str] = None
    promocode: Optional[str] = None
    message: Optional[str] = None

