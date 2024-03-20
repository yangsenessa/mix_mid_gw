from sqlalchemy.orm import Session

from dal.user_baseinfo import UserBaseInfo
from dal.work_flow_routerinfo import UserWsRootInfo

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
    userWsRootInfo = UserWsRootInfo(client_id=client_id,ws_url=ws_url,comf_url=comfyui_url,status=status)
    qry_userWsRootInfo = db.query(UserWsRootInfo).filter(UserWsRootInfo.client_id == client_id).first()
    if qry_userWsRootInfo:
        qry_userWsRootInfo.comf_url = comfyui_url
        qry_userWsRootInfo.ws_url = ws_url
        qry_userWsRootInfo.status = status
        db.commit()
        db.refresh(qry_userWsRootInfo)
    else:
        db.add(userWsRootInfo)
        db.commit()
        db.refresh(userWsRootInfo)

  

