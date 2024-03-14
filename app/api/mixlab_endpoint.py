from fastapi import APIRouter,Depends,HTTPException
from typing import Union
from models import mixlab_buss_m
from loguru import logger
import json
import datetime


import os



router = APIRouter()

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





