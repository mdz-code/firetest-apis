 
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from ...config.jwt import JwtAuth
from ...services.question_service import QuestionService
from ...database.schemas import SimulateDTO

jwe_handler = JwtAuth()
question_service = QuestionService()

from api.database.mongo_db import MongoDatabase
mongo_database = MongoDatabase()

questions = APIRouter(
    prefix="/questions"
)

@questions.post("/start", response_class=JSONResponse)
async def start(dto: SimulateDTO, user_id=Depends(jwe_handler.auth_wrapper)):
    response = await question_service.start_simulate(dto.train_mode, user_id, dto.object_infos)
    return JSONResponse(status_code=response["status"], content=response["response"])

@questions.post("/stop/{simulate_id}", response_class=JSONResponse)
async def start(simulate_id: str, user_id=Depends(jwe_handler.auth_wrapper)):
    response = await question_service.finsh_simulate(simulate_id)
    return JSONResponse(status_code=response["status"], content=response["response"])

@questions.post("/answers_feedback", response_class=JSONResponse)
async def answers(user_id=Depends(jwe_handler.auth_wrapper)):
    return { "user_id": user_id }

@questions.post("/reporter", response_class=JSONResponse)
async def reporter(user_id=Depends(jwe_handler.auth_wrapper)):
    return { "user_id": user_id }

@questions.get("/subjects", response_class=JSONResponse)
async def subjects(user_id: str = Depends(jwe_handler.auth_wrapper)):
    print('controller')
    subjects = await question_service.get_all_subjects()
    return { "subjects": subjects }

@questions.get("/{simulate_id}")
async def question(simulate_id: str):
    response = await question_service.get_question_by_simulate(simulate_id)
    return JSONResponse(status_code=response["status"], content=response["response"])
