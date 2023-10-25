from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends

from .manager import ConnectionManager
from .redisConnect import connect_redis
from .config import get_broker_config, BrokerConfig

app = FastAPI(
    version="0.1", title="Chat Service"
)


@app.on_event("startup")
async def startup_event():
    redis = await connect_redis()
    app.state.redis = redis


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, brokerConfig: BrokerConfig = Depends(get_broker_config)):
    userID = 1
    await ConnectionManager.connect(websocket)
    (channel,) = await app.state.redis.subscribe(brokerConfig.channel_name)
    try:
        while await channel.wait_message():
            message = await channel.get()
            await ConnectionManager.send_message(userID, message, websocket)
    except WebSocketDisconnect:
        channel.close()
        await ConnectionManager.disconnect(websocket)
