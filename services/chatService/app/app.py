import json
import logging
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from .manager import ConnectionManager
from .redisConnect import connect_redis
from .config import get_broker_config, BrokerConfig


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

app = FastAPI(
    version="0.1", title="Chat Service"
)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"  placeholder="message text"/>
            <input type="text" id="receiverID" autocomplete="off" placeholder="receiver ID"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:5000/chat");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var inputText = document.getElementById("messageText")
                var inputReceiverID = document.getElementById("receiverID")
                var output = {"message":inputText.value, "receiverID":receiverID.value}
                ws.send(JSON.stringify(output))
                inputText = ''
                inputReceiverID = ''
                event.preventDefault()
            }
                        
        </script>
    </body>
</html>
"""


@app.on_event("startup")
async def startup_event():
    redis = await connect_redis()
    now = datetime.datetime.now()
    logging.info(f"{now}: redis connected")


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, brokerConfig: BrokerConfig = Depends(get_broker_config)):
    """#userID = 1
    await ConnectionManager.connect(websocket)
    (channel,) = await app.state.redis.subscribe(brokerConfig.channel_name)
    try:
        while await channel.wait_message():
            #message = await channel.get()
            data = await websocket.receive_text()

            #await ConnectionManager.send_message(userID, data, websocket)
    except WebSocketDisconnect:
        channel.close()
        await ConnectionManager.disconnect(websocket)"""
    await websocket.accept()
    while True:
        now = datetime.datetime.now()
        logging.info(f"{now}: receiving...")
        data = await websocket.receive_json()
        now = datetime.datetime.now()
        logging.info(f"{now}: received")
        await websocket.send_json(data)
        now = datetime.datetime.now()
        logging.info(f"{now}: data sent {data}")


@app.get("/")
async def get():
    #currentUserID = 1 #из куки файлов или по токену
    return HTMLResponse(html)
