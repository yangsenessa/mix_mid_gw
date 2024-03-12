#user login/out domain model
from pydantic import BaseModel

# user login
class UserLoginReq(BaseModel):
    userId: str
    passWord:str

class UserLoginRsp(BaseModel):
    resultCode:str

# user regedit
class UserRegReq(BaseModel):
    logInId:str
    email:str
    cellPhone:str
    exterpriseName:str
    passWord:str

class UserRegReqRsp(BaseModel):
    resultCode:str
    userId:str


