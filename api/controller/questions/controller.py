 
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse

from ...config.jwt import JwtAuth
from ...services.question_service import QuestionService
from ...database.schemas import SimulateDTO, Reporter, FeedbackRegister

jwt_handler = JwtAuth()
question_service = QuestionService()



questions = APIRouter(
    prefix="/questions"
)

@questions.post("/start", response_class=JSONResponse)
async def start(dto: SimulateDTO, user_id=Depends(jwt_handler.auth_wrapper)):
    response = await question_service.start_simulate(dto.train_mode, user_id, dto.object_infos)
    return JSONResponse(status_code=response["status"], content=response["response"])

@questions.post("/stop/{simulate_id}", response_class=JSONResponse)
async def start(simulate_id: str, user_id=Depends(jwt_handler.auth_wrapper)):
    response = await question_service.finsh_simulate(simulate_id)
    return JSONResponse(status_code=response["status"], content=response["response"])

@questions.post("/answers_feedback", response_class=JSONResponse)
async def answers(dto: FeedbackRegister, user_id=Depends(jwt_handler.auth_wrapper)):
    response = await question_service.register_feedback(dto, user_id)
    return JSONResponse(status_code=response["status"], content=response["response"])

@questions.post("/reporter", response_class=JSONResponse)
async def reporter(dto: Reporter, user_id=Depends(jwt_handler.auth_wrapper)):
    response = await question_service.send_report(user_id, dto.question_id, dto.text_report)
    return JSONResponse(status_code=response["status"], content=response["response"])

@questions.get("/subjects", response_class=JSONResponse)
async def subjects(user_id: str = Depends(jwt_handler.auth_wrapper)):
    subjects = await question_service.get_all_subjects()
    return { "subjects": subjects }

@questions.get("/{simulate_id}")
async def question(simulate_id: str, user_id: str = Depends(jwt_handler.auth_wrapper)):
    response = await question_service.get_question_by_simulate(simulate_id, user_id)
    return JSONResponse(status_code=response["status"], content=response["response"])
