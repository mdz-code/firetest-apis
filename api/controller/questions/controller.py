 
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from api.database.mongo_db import MongoDatabase


mongo_database = MongoDatabase()

questions = APIRouter(
    prefix="/questions"
)

@questions.get("/subjects", response_class=JSONResponse)
async def subjects():
    return { "endpoint": "subjects" }

@questions.post("/start", response_class=JSONResponse)
async def start():
    return { "endpoint": "start" }

@questions.post("/answers", response_class=JSONResponse)
async def answers():
    return { "endpoint": "answers" }

@questions.post("/feedback", response_class=JSONResponse)
async def feedback():
    return { "endpoint": "feedback" }

@questions.post("/reporter", response_class=JSONResponse)
async def reporter():
    return { "endpoint": "reporter" }

@questions.get("/{question_id}")
async def question(question_id: str):
    inserted = await mongo_database.insert_one('questions', { "question": question_id}, True)
    founded = await mongo_database.get_one('questions', { "_id": inserted})
    print(founded)

    updated = await mongo_database.update_one('questions', { "_id": inserted}, { "$set": { "question": f"{question_id}123456" } })
    founded = await mongo_database.get_one('questions', { "_id": inserted})
    print(founded)


    

    return dict(founded)