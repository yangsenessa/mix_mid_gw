from typing import List

from fastapi import APIRouter,Depends, WebSocket, WebSocketDisconnect
from models import mixlab_buss_m
from dal.work_flow_routerinfo import WorkFlowRouterInfo
from starlette.requests import HTTPConnection
from websocket import WebSocketApp
from database import SessionLocal,engine
from sqlalchemy.orm import Session


from api import mixlab_endpoint

from loguru import logger


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

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str,db: Session = Depends(get_db)):

    await manager.connect(websocket)
    (node,comfyui_url, ws_url) = mixlab_endpoint.init_user_router(db, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            mixlab_endpoint.detail_recall(websocket.url,client_id,data,db)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户-{user}-离开")
