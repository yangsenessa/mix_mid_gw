from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

from database import Base

class WorkFlowRouterInfo(Base):
    __tablename__ = "tb_workflow_routerinfo"
    client_id = Column(String, primary_key=True)
    prompts_id = Column(String)
    user_id = Column(String)
    input_keys = Column(String)
    output_keys = Column(String)
    comfyui_url = Column(String)
    status = Column(String)
    gmt_datetile = Column(DateTime)


class  ComfyuiNode(Base):
    __tablename__ = "tb_comfyui_node"
    node_id = Column(String,primary_key=True)
    url = Column(String)
    port = Column(String)
    weight = Column(String)

