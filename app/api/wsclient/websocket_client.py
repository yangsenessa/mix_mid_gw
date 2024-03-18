import websockets
import asyncio
from loguru import logger
from api import mixlab_endpoint
from sqlalchemy.orm import Session

import json
import random

class ComfyuiEvent:
    onStatusChanged = []
    @staticmethod
    def raiseEvent(sid,args,db):
        for fun in ComfyuiEvent.onStatusChanged:
            fun(sid,args,db)



# The main function that will handle connection and communication
# with the server
async def ws_client(url,db:Session):
    logger.debug("WebSocket: Client Connected.")
    if url == None:
       url = "ws://127.0.0.1:7890"
    sid =url.split("=")[1]
    #relurl = url.split("=")[0]+"="+genersid()
    relurl = url
    logger.debug("sid="+sid)
    logger.debug("relurl="+ relurl)
    # Connect to the server
    async with websockets.connect(relurl) as ws:
 
        while True:
            msg = await ws.recv()
            print("WS:JSON:ORI:"+msg)
            #body = json.loads(msg)
           # logger.debug("WS:JSON:",json.dumps(body))
            ComfyuiEvent.raiseEvent(sid,msg,db)
                      

# Start the connection
def run_wsclient(url:str | None,db:Session):
    ComfyuiEvent.onStatusChanged.append(mixlab_endpoint.executed)
    asyncio.run(ws_client(url,db))



def genersid():
  res = []
  for i in range(20):
      x = random.randint(1,2)
      if x == 1:
          y = str(random.randint(0,9))
      else:
          y = chr(random.randint(97,122))
      res.append(y)
  res = ''.join(res)
  logger.debug("random="+res)
  return res