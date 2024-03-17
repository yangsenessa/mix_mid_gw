from sqlalchemy.orm import Session
from dal.work_flow_routerinfo import WorkFlowRouterInfo,ComfyuiNode

def create_wk_router(db:Session, wkrouter:WorkFlowRouterInfo):
    db.add(wkrouter)
    db.commit()
    db.refresh(wkrouter)
    return wkrouter

def update_wk_router(db:Session, client_id:str,prompts_id:str,status:str,body:str):
    db_wkrouter = db.query(WorkFlowRouterInfo).filter(
                       WorkFlowRouterInfo.client_id == client_id
                           ,WorkFlowRouterInfo.prompts_id == prompts_id).first()
    
    db_wkrouter.status=status
    
    db.commit()
    db.refresh(db_wkrouter)
    return db_wkrouter

def get_wk_router_clientid_promptid(db:Session, client_id:str, prompt_id:str):
    db_wkrouter = db.query(WorkFlowRouterInfo).filter(
        WorkFlowRouterInfo.client_id ==  client_id, WorkFlowRouterInfo.prompts_id == prompt_id
    ).first()
    return db_wkrouter

def get_comfyui_node(db:Session):
    node = db.query(ComfyuiNode).order_by(ComfyuiNode.weight).first()
    return node

def add_comfyui_weight(db:Session, node:ComfyuiNode):
    node.weight = node.weight+1
    db.commit()
    db.refresh(node)
    return node