from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.responses import JSONResponse

from models import mixlab_buss_m, user_login_m
from dal.work_flow_routerinfo import WorkFlowRouterInfo,ComfyuiNode

from loguru import logger
from urllib.parse import urlencode
from sqlalchemy.orm import Session
from dal import user_baseinfo, user_crud, work_flow_crud
from database import SessionLocal, engine

import requests
import json
from datetime import datetime
from api.wsclient import websocket_client
import threading
import os



router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/mixlab/workflow")
def query_workflow(request:mixlab_buss_m.WorkflowQuery):
    filename = request.filename
    category = request.category
    data = []
    current_path = os.path.abspath(os.path.dirname(__file__))
    app_path=os.path.join(current_path, "workflows")
    category_path=os.path.join(app_path,category)
    if not os.path.exists(category_path):
        os.mkdir(category_path)
    logger.debug(app_path)
    app_workflow_path=os.path.join(app_path, filename)
    try:
        with open(app_workflow_path) as json_file:
            json_data = json.load(json_file)
        
            apps = [{
                'filename':filename,
                'data':json_data
                }]
    except Exception as e:
        logger.error("发生异常：", str(e))
    if len(apps)==1 and category!='' and category!=None:
        data=read_workflow_json_files(category_path)
            
        for item in data:
            x=item["data"]
            # print(apps[0]['filename'] ,item["filename"])
            if apps[0]['filename']!=item["filename"]:
                category=''
                input=None
                output=None
                if 'category' in x['app']:
                    category=x['app']['category']
                if 'input' in x['app']:
                    input=x['app']['input']
                if 'output' in x['app']:
                    output=x['app']['output']
                apps.append({
                    "filename":item["filename"],
                    # "category":category,
                    "data":{
                        "app":{
                            "category":category,
                            "description":x['app']['description'],
                            "filename":(x['app']['filename'] if 'filename' in x['app'] else "") ,
                            "icon":(x['app']['icon'] if 'icon' in x['app'] else None),
                            "name":x['app']['name'],
                            "version":x['app']['version'],
                            "input":input,
                            "output":output
                        }
                    },
                    "date":item["date"]
                })

    

    return apps
# workflow  
def read_workflow_json_files(folder_path ):
    json_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            json_files.append(filename)

    data = []
    for file in json_files:
        file_path = os.path.join(folder_path, file)
        try:
            with open(file_path) as json_file:
                json_data = json.load(json_file)
                creation_time=datetime.datetime.fromtimestamp(os.path.getctime(file_path))
                numeric_timestamp = creation_time.timestamp()
                file_info = {
                    'filename': file,
                    'data': json_data,
                    'date': numeric_timestamp
                }
                data.append(file_info)
        except Exception as e:
            print(e)
    sorted_data = sorted(data, key=lambda x: x['date'], reverse=True)
    return sorted_data

#prompt
@router.post("/mixlab/prompt")
async def do_prompts_process(request:Request,db:Session = Depends(get_db)):
    
    try:
       body = await request.json()
       re_requestbody = json.dumps(body)
    except:
        raise HTTPException(status_code=400,detail="Invaid JSON format")
    logger.debug(re_requestbody)
    #check userInfo
    user_dao = user_crud.get_user(db,body['client_id'])
    if user_dao:
       logger.debug("Authoried user")
    else:
        raise HTTPException(status_code=400,detail="Invaid user")

    re_headers = {
    "Content-Type": "application/json"
    }
    logger.debug(request.headers)
    #Get node
    node = work_flow_crud.get_comfyui_node(db)

    response = requests.post("http://"+node.host+":"+node.port+"/"+node.url,json=body,headers=re_headers)
    logger.debug(response.content)
    logger.debug(response.headers)

    try:
        re_response = response.json()
        if re_response["prompt_id"]:
           wk_info =  WorkFlowRouterInfo()  
           wk_info.prompts_id = re_response["prompt_id"]
           wk_info.client_id = user_dao.user_id
           wk_info.status="progress"
           wk_info.gmt_datetime =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           work_flow_crud.create_wk_router(db,wk_info)
           work_flow_crud.add_comfyui_weight(db,node)   
           logger.debug("open ws socket")
           ws_url = "ws://"+node.host+":"+node.port+"/ws?clientId="+user_dao.user_id
           t1 = threading.Thread(target=websocket_client.run_wsclient, args=(ws_url,))
           t1.start()
           #websocket_client.run_wsclient(ws_url)    
    except Exception as e:
        print(e)
        logger.debug("some exception")
    #res =json.dumps(response)

    return re_response    

async def executed(sid:str,msg:dict):
    db = get_db()
    status:str
    if "type" in msg.keys():
       status = msg["type"]
    elif "output" in msg.keys():
       status = "executed"
    else:
       logger.debug("unknow event")
       return
    logger.debug("status:"+status)

    logger.debug("recall:"+json.dumps(msg))
    if status == "status":
        logger.debug("RETURN")
        return 
    data:dict
    data = msg[data]
    if "prompt_id" in  data.keys:
        try:
           prompt_id = msg["data"]["prompt_id"]    
           logger.debug("prompt_id:"+prompt_id)
           logger.debug("msg=",json.dumps(msg))

           work_flow_crud.update_wk_router(db,sid,prompt_id,status,json.dumps(msg))
        except Exception as e:
           print(e)
           logger.debug("db exception")
 
    return 
   
    




    

      







