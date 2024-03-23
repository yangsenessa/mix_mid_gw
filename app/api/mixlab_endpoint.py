from fastapi import APIRouter,Depends,HTTPException,Request
from fastapi.responses import JSONResponse

from models import mixlab_buss_m, user_login_m
from dal.work_flow_routerinfo import WorkFlowRouterInfo,ComfyuiNode
from dal.user_baseinfo import UserWsRouterInfo

from loguru import logger
from urllib.parse import urlencode
from sqlalchemy.orm import Session
from dal import user_baseinfo, user_crud, work_flow_crud
from database import SessionLocal, engine

import requests
import json
from datetime import datetime
from api.wsclient import websocket_client
from api.wsclient.websocket_client_new import WebsocetClient
import time
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
def query_workflow(request:mixlab_buss_m.WorkflowQuery,db:Session = Depends(get_db)):
    filename = request.filename
    category = request.category
    client_id = request.token
    data = []
     #check userInfo
    user_dao = user_crud.get_user(db,client_id)
    if user_dao:
       logger.debug("Authoried user")
    else:
        raise HTTPException(status_code=400,detail="Invaid user")

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
       body =await request.json()
       re_requestbody = json.dumps(body)
    except Exception as e:
        print(e)
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
    user_ws_router:UserWsRouterInfo

    user_ws_router = user_crud.fetch_user_ws_router(db,body["client_id"])
    if(user_ws_router) :
        comf_url = user_ws_router.comf_url
        ws_url = user_ws_router.ws_url
    else:
        raise HTTPException(status_code=400,detail="Invaid user")
    try:   
        logger.debug("begin create ws client")
        t1=threading.Thread(target=WebsocetClient().start,args=(body["client_id"],ws_url,db))
        t1.start()
        time.sleep(2)
        logger.debug("begin post:" + "  "+ comf_url)
    
        
        response = requests.post(comf_url,json=body,headers=re_headers)

        re_response =  response.json()
        logger.debug("re_response -- ",json.dumps(re_response))

        wk_info =  WorkFlowRouterInfo()  
        wk_info.prompts_id = re_response["prompt_id"]
        wk_info.client_id = user_dao.user_id
        wk_info.status="progress"
        wk_info.comfyui_url=comf_url
        wk_info.gmt_datetime =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        work_flow_crud.create_wk_router(db,wk_info)
       
        logger.debug(response.content)
        logger.debug(response.headers)
           
    except Exception as e:
        print(e)
        logger.debug("some exception")
    #res =json.dumps(response)

    return re_response   

def queue(url:str, head:Request.headers):
    queue_info = []
    try:
        while True:
            response = requests.get(url,headers=head).text
            logger.debug(response)
            queue_info = json.loads(response)
            if(queue_info["exec_info"]["queue_remaining"] == 0):
                logger.debug("QUEUE STOP")
                break
    except Exception as e:
       logger.debug("QUEUE Exception")
       print(e)


def detail_recall(url:str,sid:str,detail:str,db:Session):
    status:str
    msg = json.loads(detail)
    if "type" in msg.keys():
       status = msg["type"]
   
    logger.debug("status:"+status)
    logger.debug("recall:"+json.dumps(msg))
    
    data:dict
    output:dict
    data = msg["data"]
    if "output" in data.keys():
        output = data["output"]
        logger.debug("recall...")
    else:
        return False
    if  "images" in output.keys():
        filenames = json.dumps(output["images"])
    elif  "text" in output.keys():
        filenames = json.dumps(output["text"])
    elif  "gifts" in output.keys():
        filenames = json.dumps(output["gifts"])
    else:
        return False

    if ("prompt_id" in  data.keys()):
        try:
           prompt_id = msg["data"]["prompt_id"]    
           logger.debug("prompt_id:"+prompt_id)
           filenames = json.dumps(data["output"]["images"])
           logger.debug("filenames="+ filenames)
           work_flow_crud.update_wk_router(db,sid,prompt_id,filenames,url,status)
        except Exception as e:
           print(e)
           logger.debug("db exception")
 
    return True


   
    




    

      







