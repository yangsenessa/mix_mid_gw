from typing import Union

from fastapi import FastAPI
from api import usermanner_endpoint
from api import mixlab_endpoint
from loguru import logger
import uvicorn
from api.wsclient import websocket_client
import mysql.connector
from database import SessionLocal

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


 

app = FastAPI()

app.include_router(usermanner_endpoint.router)
app.include_router(mixlab_endpoint.router)

#app.include_router(items.router)
#app.include_router(
 #   admin.router,
  #  prefix="/admin",
   # tags=["admin"],
   # dependencies=[Depends(get_token_header)],
  #  responses={418: {"description": "I'm a teapot"}},
#)
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
mydb = mysql.connector.connect(
        host="mixlib-mid-gw.rwlb.rds.aliyuncs.com",       # 数据库主机地址
        user="mixlabdb",    # 数据库用户名
        passwd="mixlab_DB",   # 数据库密码
        database="mixlabdb"
      )
mycursor = mydb.cursor()
db = SessionLocal()
def init_router():
    #print("Thread ws scanning")
    mycursor.execute("SELECT client_id, ws_url FROM `tb_user_ws_root` where `status` ='INIT'")
    myresult = mycursor.fetchall()
    if myresult.count == 0:
       return     

    for x in myresult:
      print("Create ws socket id="+x[1])
      mycursor.execute("UPDATE `tb_user_ws_root` set `status` ='ACTIVATE' where client_id='" + x[0] +"'")
      mydb.commit()
      websocket_client.run_wsclient(x[1],"",db)
     
    
jobstores = {'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')}
scheduler = AsyncIOScheduler(jobstores=jobstores)
#scheduler.start()
print("scheduler starting...")

#scheduler.add_job(init_router, "interval",max_instances=10, seconds=5)  
#asyncio.get_event_loop().run_forever() 
print("scheduler added...")

if __name__ == '__main__':
   uvicorn.run(app)
    
   # t1 = threading.Thread(target=websocket_client.run_wsclient, args=(ws_url,))
   # t2= threading.Thread(target=uvicorn.run,args=(app,))
   # t1.start()
   # t2.start()
   
         
