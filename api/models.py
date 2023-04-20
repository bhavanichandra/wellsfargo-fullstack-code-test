from datetime import datetime

from pydantic import BaseModel


class Login(BaseModel):
    email: str
    name: str


class User(BaseModel):
    user_id: str
    name: str
    email: str


class Session(BaseModel):
    session_id: str
    user_id: str
    timestamp: datetime
