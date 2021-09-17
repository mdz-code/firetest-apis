
from fastapi import Depends, APIRouter, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer

from sqlalchemy.orm.session import Session

from ...config.jwt import JwtAuth
from ...database import schemas, postgres_sql
from ...config.postgres import SessionLocal
from ...services.user_service import UserService



# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


jwt_auth = JwtAuth()
security_token = HTTPBearer()

user_services = UserService()


users = APIRouter(
    prefix="/users"
)

@users.get("/current_user")
async def current_user(user_id: str = Depends(jwt_auth.auth_wrapper), db: Session = Depends(get_db)):
    response = user_services.get_current_user(user_id, db)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.post("/create")
async def get(dto: schemas.UserDTO, db: Session = Depends(get_db)):
    response = user_services.store_new_user(dto, db)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.post('/recover', response_class=JSONResponse)
async def recover_user(email: schemas.RecoverUser, db: Session = Depends(get_db)):
    response = user_services.recover_user(email, db)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.get('/recover/{uuid}', response_class=JSONResponse)
async def recover_user(uuid: str, db: Session = Depends(get_db)):
    response = user_services.get_recover_user(uuid, db)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.post("/login", response_class=JSONResponse)
async def get(user: schemas.UserAuth, db: Session = Depends(get_db)):
    response = user_services.auth_user(user, db)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.post("/logout", response_class=JSONResponse)
async def get(token: str = Security(security_token)):
    response = user_services.logout_user(token.credentials)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.patch("/update", response_class=JSONResponse)
async def update(user: schemas.UserUpdate, user_id: str = Depends(jwt_auth.auth_wrapper), db: Session = Depends(get_db)):
    response = user_services.update_user(user_id, user, db)
    return JSONResponse(status_code=response["status"], content=response["response"])

@users.get("/feedback", response_class=JSONResponse)
async def get():
    return {"endpoint": "feedback"}




