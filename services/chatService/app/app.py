from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
from .test_html_page import template
from .database import create_table
from .models import Message
from .websocket_manager import get_messages, send_message


app = FastAPI()

create_table()

connected_clients = []


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connected_clients.append(websocket)

    messages = get_messages(user_id)
    for message in messages:
        await websocket.send_json(message)
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(**json.loads(data))
            send_message(websocket, message)

            for client in connected_clients:
                if client != websocket:
                    await client.send_text(message)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)




@app.get("/test_chat/{user_id}", response_class=HTMLResponse)
async def test_chat(user_id: str):
    return HTMLResponse(content=template.render(user_id=user_id))
