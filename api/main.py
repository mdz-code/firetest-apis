from fastapi import FastAPI, APIRouter
from .controller.questions.controller import questions
from .controller.users.controller import users


app = FastAPI()

app.include_router(questions)
app.include_router(users)
