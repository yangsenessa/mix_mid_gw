from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class UserBaseInfo(Base):
    __tablename__ = "tb_user_baseinfo"
    user_id = Column(String, primary_key=True)
    nick_name = Column(String)
    email = Column(String)
    cell_phone = Column(String)
    exterprisename = Column(String)
    password = Column(String)


