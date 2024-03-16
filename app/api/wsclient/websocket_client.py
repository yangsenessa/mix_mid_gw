import websockets
import asyncio

# The main function that will handle connection and communication
# with the server
async def ws_client(url):
    print("WebSocket: Client Connected.")
    if url == None:
       url = "ws://127.0.0.1:7890"
    # Connect to the server
    async with websockets.connect(url) as ws:
      
        #await ws.send(f"{name}")
        #await ws.send(f"{age}")

        # Stay alive forever, listen to incoming msgs
        while True:
            msg = await ws.recv()
            print(msg)

# Start the connection
def run_wsclient(url:str | None):
    asyncio.run(ws_client(url))