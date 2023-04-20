from typing import Annotated

import pandas as pd
from fastapi import FastAPI, UploadFile, Body, Response, Header

from models import Login
from utility.builders import response_builder, new_session, new_user, new_mongo_data_set
from utility.database import get_collection

app = FastAPI()


@app.post('/user')
def create_user(login: Login, response: Response):
    try:
        user_col = get_collection("users")
        existing_user = user_col.find({"email": login.email, "name": login.name})
        if dict(existing_user):
            return response_builder(404, login, "User already exist")
        user = new_user(name=login.name, email=login.email)
        user_col.insert_one(dict(user))
        response.status_code = 201
        return response_builder(200, dict(user), "New User added")
    except Exception as ex:
        response.status_code = 500
        return response_builder(500, None, str(ex))


@app.post('/new-session')
def create_user_session(body: Annotated[dict[str, str], Body()], response: Response):
    try:
        email = body.get('email')
        user_col = get_collection("users")
        user = user_col.find_one({"email": email})
        if not dict(user):
            return response_builder(404, email, "User doesn't exist")
        session_col = get_collection("sessions")
        session = session_col.find_one({"user_id": user.get('user_id')})
        user_dict = dict(user)
        if not session:
            session = new_session(user_dict.get('user_id'), email)
            session_dict = dict(session)
            session_col.insert_one(dict(session))
        else:
            session_dict = dict(session)
        response.status_code = 201
        return response_builder(200, session_dict.get('session_id'), "Session Generated")
    except Exception as ex:
        response.status_code = 500
        return response_builder(500, None, str(ex))


@app.post('/upload')
async def upload_data_set(file: UploadFile, session_id: str, response: Response):
    try:
        session_col = get_collection("sessions")
        session = session_col.find_one({"session_id": session_id})
        dataset_collection = get_collection("datasets")
        data = pd.read_csv(file.file)
        list_dict = data.to_dict(orient="records")
        mongo_record = new_mongo_data_set(session.get('user_id'), session_id, list_dict)
        dataset_collection.insert_one(mongo_record)
        response.status_code = 200
        return response_builder(200, None, "Upload to db")
    except Exception as ex:
        response.status_code = 500
        return response_builder(500, None, str(ex))


@app.get("/records")
def get_records(session_id: Annotated[str | None, Header()], response: Response):
    try:
        session_col = get_collection("sessions")
        session = session_col.find_one({"session_id": session_id})
        if not session:
            response.status_code = 400
            return response_builder(400, None, "Invalid Session")
        user_id = session.get("user_id")
        dataset_collection = get_collection("datasets")
        data_set_obj = dataset_collection.find_one({"user_id": user_id})
        data_set = data_set_obj.get('data_set')
        return response_builder(200, data_set, "Fetched data")
    except Exception as ex:
        response.status_code = 500
        return response_builder(500, None, str(ex))
