from typing import Union

from fastapi import FastAPI
from api import usermanner_endpoint
from api import mixlab_endpoint
from api import wsserver_endpoint
from loguru import logger
import uvicorn



app = FastAPI()

app.include_router(usermanner_endpoint.router)
app.include_router(mixlab_endpoint.router)
app.include_router(wsserver_endpoint.router)

#app.include_router(items.router)
#app.include_router(
 #   admin.router,
  #  prefix="/admin",
   # tags=["admin"],
   # dependencies=[Depends(get_token_header)],
  #  responses={418: {"description": "I'm a teapot"}},
#)
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



if __name__ == '__main__':
   uvicorn.run(app)
    
   # t1 = threading.Thread(target=websocket_client.run_wsclient, args=(ws_url,))
   # t2= threading.Thread(target=uvicorn.run,args=(app,))
   # t1.start()
   # t2.start()
   
         
