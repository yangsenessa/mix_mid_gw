from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from dal import user_baseinfo, user_crud
from database import SessionLocal,engine
from loguru import logger


from models import user_login_m

router = APIRouter()
user_baseinfo.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}


@router.post("/userLogin",response_model=user_login_m.UserLoginRsp)
def userLogin(user_login_req : user_login_m.UserLoginReq, db: Session = Depends(get_db)):
    user_dao =  user_crud.get_user_by_login_id(db,user_login_req.loginId)
    user_login_rsp = user_login_m.UserLoginRsp();
    if user_dao == None :
       logger.debug("user_dao is null")
       user_login_rsp.resultCode="FAIL"
     
    user_login_rsp.resultCode="SUCCESS"
    return user_login_rsp