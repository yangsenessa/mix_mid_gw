from sqlalchemy.orm import Session

from dal.user_baseinfo import UserBaseInfo

def get_user(db: Session, login_id: str):
    return db.query(UserBaseInfo).filter(UserBaseInfo.login_id == login_id).first()

def create_user(db: Session, user: UserBaseInfo):
    
    db_user = user
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(UserBaseInfo).filter(UserBaseInfo.email == email).first()

def get_user_by_login_id(db:Session, login_id:str):
    return db.query(UserBaseInfo).filter(UserBaseInfo.login_id == login_id).first()


