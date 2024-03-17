import websockets
import asyncio
from loguru import logger
from api import mixlab_endpoint
import json
import random


# The main function that will handle connection and communication
# with the server
async def ws_client(url):
    logger.debug("WebSocket: Client Connected.")
    if url == None:
       url = "ws://127.0.0.1:7890"
    sid =url.split("=")[1]
    relurl = url.split("=")[0]+"="+genersid()
    logger.debug("sid="+sid)
    logger.debug("relurl="+ relurl)
    # Connect to the server
    async with websockets.connect(relurl) as ws:
      
        #await ws.send(f"{name}")
        #await ws.send(f"{age}")

        # Stay alive forever, listen to incoming msgs
        while True:
            msg = await ws.recv()
            logger.debug(msg)
            body = json.loads(msg)
            await mixlab_endpoint.executed(sid,body)
               

# Start the connection
def run_wsclient(url:str | None):
    asyncio.run(ws_client(url))

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