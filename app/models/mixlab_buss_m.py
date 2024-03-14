# Buss domain models
from pydantic import BaseModel

#/mixlab/workflow
class WorkflowQuery(BaseModel):
    task:str
    filename:str
    category:str|None = None
