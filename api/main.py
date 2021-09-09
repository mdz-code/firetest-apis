import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from .controller.questions.controller import questions
from .controller.users.controller import users
from .config.variables import variables_enviroment

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions)
app.include_router(users)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port= variables_enviroment['port'] | 5000)