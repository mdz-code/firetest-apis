import uvicorn
from fastapi import FastAPI, APIRouter
from .controller.questions.controller import questions
from .controller.users.controller import users
from .config.variables import variables_enviroment

app = FastAPI()

app.include_router(questions)
app.include_router(users)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port= variables_enviroment['port'] | 5000)