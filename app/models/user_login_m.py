#user login/out domain model
from pydantic import BaseModel

class UserLoginReq(BaseModel):
    userId: str
    passWord:str

