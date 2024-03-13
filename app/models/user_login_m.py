#user login/out domain model
from pydantic import BaseModel

# user login
class UserLoginReq(BaseModel):
    loginId: str
    passWord:str

class UserLoginRsp(BaseModel):
    resultCode:str | None = None

# user regedit
class UserRegReq(BaseModel):
    loginId:str
    nickName:str | None = None
    email:str | None = None
    cellPhone:str | None = None
    exterpriseName:str | None = None
    passWord:str | None = None

class UserRegReqRsp(BaseModel):
    resultCode:str
    userId:str


