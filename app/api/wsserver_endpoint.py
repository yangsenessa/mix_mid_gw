from typing import List

from fastapi import APIRouter,Depends, WebSocket, WebSocketDisconnect
from models import mixlab_buss_m
from dal.work_flow_routerinfo import WorkFlowRouterInfo
from dal import work_flow_crud
from starlette.requests import HTTPConnection
from database import SessionLocal,engine
from sqlalchemy.orm import Session


from api import mixlab_endpoint

from loguru import logger
import time


router = APIRouter()


class ConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: List[WebSocket] = []

    def creatWsClient(url:str):
        conn = HTTPConnection
        
    
    async def connect(self, ws: WebSocket):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove(ws)

    @staticmethod
    async def send_personal_message(message: str, ws: WebSocket):
        # 发送个人消息
        await ws.send_text(message)

    async def broadcast(self, message: str):
        # 广播消息
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.websocket("/ws/{client_id}{prompt_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str,prompt_id,db: Session = Depends(get_db)):

    await manager.connect(websocket)
    
    try:
        while True:
            time.sleep(1)
            workFlowRouterInfo = work_flow_crud.get_wk_router_clientid_promptid(db,client_id,prompt_id)
            if workFlowRouterInfo:
                websocket.send_json(workFlowRouterInfo.ori_body)
                if(len(workFlowRouterInfo.filenames)):
                    websocket.close()

    except WebSocketDisconnect:
        manager.disconnect(websocket)