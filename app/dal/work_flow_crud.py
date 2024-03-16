from sqlalchemy.orm import Session
from dal.work_flow_routerinfo import WorkFlowRouterInfo,ComfyuiNode

def create_wk_router(db:Session, wkrouter:WorkFlowRouterInfo):
    db.add(wkrouter)
    db.commit()
    db.refresh()
    return wkrouter

def update_wk_router(db:Session, wkrouter:WorkFlowRouterInfo):
    db_wkrouter = db.query(WorkFlowRouterInfo).filter(
                       WorkFlowRouterInfo.client_id == wkrouter.client_id
                           ,WorkFlowRouterInfo.prompts_id == wkrouter).first()
    if wkrouter.input_keys:
        db_wkrouter.input_keys = wkrouter.input_keys
    
    if wkrouter.output_keys:
        db_wkrouter.output_keys = wkrouter.output_keys
    
    db.commit()
    db.refresh(db_wkrouter)
    return db_wkrouter