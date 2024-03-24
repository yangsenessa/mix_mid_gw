# -*- coding:utf-8 -*-
import websocket
from database import Database
from sqlalchemy.orm import Session
import json
from loguru import logger
from api import mixlab_endpoint
from api import wsserver_endpoint
import threading
import time

database = Database()
engine = database.get_db_connection()





class WebsocetClient(object):
    def __init__(self):
        super(WebsocetClient, self).__init__()
        self.url = "ws://echo.websocket.org/"
        self.ws = None
        self.db = None
        self.sid =None
        

    def on_message(self, source,message):
        if self.if_execute_type(message):
            if  mixlab_endpoint.detail_recall(self.url,self.sid,message,self.db):
                self.ws.close()

        print("####### on_message #######")
        print("message：%s" % message)

    def on_error(self,*error):
        print("####### on_error #######")
        print("error：" + str(error) )

    def on_close(self,source,close_status_code,close_msg):
        print("####### on_close #######")

    def on_ping(self, message):
        print("####### on_ping #######")
        print("ping message：%s" % message)

    def on_pong(self, message):
        print("####### on_pong #######")
        print("pong message：%s" % message)

    def on_open(self,*message):
        print("####### on_open #######")

    def run(self, sid:str,detail:str,db:Session):
        while True:
            time.sleep(1)
           
    def if_execute_type(self,message):
        status:str
        detail_json = json.loads(message)
        if "type" in  detail_json.keys():
            status=detail_json["type"]
        
        return "status" != status


    def start(self,client_id:str,ws_url:str,db:Session):
    
        logger.debug("Begin create WebSocketApp:" + ws_url)
        self.ws = websocket.WebSocketApp(ws_url,
                               on_open=self.on_open,
                               on_message=self.on_message,
                               on_error=self.on_error,
                               on_close=self.on_close)
        database =  Database()
        self.db = database.get_db()
        self.url = ws_url
        self.sid = client_id
        # self.ws.on_open = self.on_open  # 也可以先创建对象再这样指定回调函数。run_forever 之前指定回调函数即可。
        #threading.Thread(target=self.ws.run_forever()) 
        self.ws.run_forever()


#if __name__ == '__main__':
#    Test().start()

"""
--- request header ---
GET / HTTP/1.1
Upgrade: websocket
Host: echo.websocket.org
Origin: http://echo.websocket.org
Sec-WebSocket-Key: AXR9yvs3Ucn9LE35KkhXfw==
Sec-WebSocket-Version: 13
Connection: upgrade


-----------------------
--- response header ---
HTTP/1.1 101 Web Socket Protocol Handshake
Connection: Upgrade
Date: Wed, 04 Aug 2021 06:29:05 GMT
Sec-WebSocket-Accept: WoOPLeAQpWaV2Bqd4sDOFkSpUuw=
Server: Kaazing Gateway
Upgrade: websocket
-----------------------
####### on_open #######
输入要发送的消息（ps：输入关键词 close 结束程序）:
aaadbbbbb
send: b'\x81\x89\x82-\xdfj\xe3L\xbe\x0e\xe0O\xbd\x08\xe0'
####### on_message #######
message：aaadbbbbb
输入要发送的消息（ps：输入关键词 close 结束程序）:
sakdnakjf
send: b'\x81\x89\xa8\xe0g\x8b\xdb\x81\x0c\xef\xc6\x81\x0c\xe1\xce'
####### on_message #######
message：sakdnakjf
输入要发送的消息（ps：输入关键词 close 结束程序）:
123456
send: b'\x81\x86(\x84>\xb7\x19\xb6\r\x83\x1d\xb2'
####### on_message #######
message：123456
输入要发送的消息（ps：输入关键词 close 结束程序）:
send: b'\x8a\x80.\xf3`+'
send: b'\x8a\x80P\x0c\xc6W'
send: b'\x8a\x807j\x03l'
send: b'\x8a\x80\xd0\xac%v'
send: b'\x8a\x80\xb9\x9do\x08'
send: b'\x8a\x80s\xbb\xad\x8f'
send: b'\x8a\x80\xf4-\xd9\x8b'
close
send: b'\x88\x82\xf5L>\xc4\xf6\xa4'
####### on_close #######

Process finished with exit code 0

"""
