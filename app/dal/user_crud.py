from sqlalchemy.orm import Session

from dal.user_baseinfo import UserBaseInfo,UserWsRouterInfo

from loguru import logger

def get_user(db: Session, client_id: str):
    return db.query(UserBaseInfo).filter(UserBaseInfo.user_id == client_id).first()

def create_user(db: Session, user: UserBaseInfo):
    
    db_user = user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(UserBaseInfo).filter(UserBaseInfo.email == email).first()

def get_user_by_cellphone(db:Session, cellphone:str):
    return db.query(UserBaseInfo).filter(UserBaseInfo.cell_phone == cellphone).first()

# init user router infu
def create_update_user_route_info(db:Session,client_id:str,ws_url:str, comfyui_url:str, status:str):
    userWsRouterInfo = UserWsRouterInfo(client_id=client_id,ws_url=ws_url,comf_url=comfyui_url,status=status)
    qry_userWsRouterInfo = db.query(UserWsRouterInfo).filter(UserWsRouterInfo.client_id == client_id).first()
    if qry_userWsRouterInfo:
        qry_userWsRouterInfo.comf_url = comfyui_url
        qry_userWsRouterInfo.ws_url = ws_url
        qry_userWsRouterInfo.status = status
        db.commit()
        db.refresh(qry_userWsRouterInfo)
        userWsRouterInfo = qry_userWsRouterInfo
    else:
        db.add(userWsRouterInfo)
        db.commit()
        db.refresh(userWsRouterInfo)
    return userWsRouterInfo
    
# No need validation the status, connect would be reused,but there is other function should
# be generrated to confirm the user only can maintail one router during certain session
def fetch_user_ws_router(db:Session, client_id:str):
    qry_userWsRouterInfo = db.query(UserWsRouterInfo).filter(UserWsRouterInfo.client_id == client_id).first()
    return qry_userWsRouterInfo
  

def update_user_ws_status(db:Session, client_id:str, status:str):
        qry_userWsRouterInfo = db.query(UserWsRouterInfo).filter(UserWsRouterInfo.client_id == client_id).first()
        if qry_userWsRouterInfo:
            qry_userWsRouterInfo.status = status
            db.commit()
            db.refresh(qry_userWsRouterInfo)
        else:
            logger.error("update user_ws_router ,entity not exist" + client_id)