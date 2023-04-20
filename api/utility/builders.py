from datetime import datetime
from uuid import uuid4

from models import User, Session


def response_builder(status, data, message):
    return {"success": status == 200, "data": data, "message": message}


def new_user(name: str, email: str):
    user = User(name=name, email=email, user_id=uuid4().hex)
    return user


def new_session(user_id: str, email: str):
    session = Session(email=email, user_id=user_id, session_id=uuid4().hex, timestamp=datetime.now())
    return session


def new_mongo_data_set(user_id: str, session_id: str, data_set: list[dict[int, int]]):
    return {"user_id": user_id, "session_id": session_id, "data_set": data_set}
