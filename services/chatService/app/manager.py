from fastapi import WebSocket
import json


class ConnectionManager:
    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()

    @staticmethod
    async def disconnect(websocket: WebSocket):
        await websocket.close()

    @staticmethod
    async def send_message(userID: int, message: bytes, websocket: WebSocket):
        message = json.loads(message.decode("utf-8"))
        receiverID = message.get("receiverID")
        senderID = message.get("senderID")
        messageObject = message.get("message", {})
        if userID == senderID or userID == receiverID:
            await websocket.send_json(messageObject)
