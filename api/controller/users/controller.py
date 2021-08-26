
from fastapi import Depends, APIRouter
from fastapi.responses import JSONResponse
from api.config.jwt import JwtAuth

jwt_auth = JwtAuth()

users = APIRouter(
    prefix="/users"
)

@users.post("/create", response_class=JSONResponse)
async def get():
    return {"endpoint": "create"}

@users.post("/login", response_class=JSONResponse)
async def get():
    return {"endpoint": "login"}

@users.post("/recover", response_class=JSONResponse, dependencies=[Depends(jwt_auth.verify_token)])
async def get():
    return {"endpoint": "recover"}

@users.post("/logout", response_class=JSONResponse)
async def get():
    return {"endpoint": "logout"}

@users.get("/feedback", response_class=JSONResponse)
async def get():
    return {"endpoint": "feedback"}

@users.patch("/update", response_class=JSONResponse)
async def get():
    return {"endpoint": "update"}


