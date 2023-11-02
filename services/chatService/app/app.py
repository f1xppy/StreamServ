from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json
from jinja2 import Template
import pymysql.cursors
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

app = FastAPI()

mysql_connection = pymysql.connect(
    host="localhost",
    user="streamserv",
    password="streamserv",
    database="streamserv",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = mysql_connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS messages (id int(10) AUTO_INCREMENT PRIMARY KEY, sender VARCHAR(50), receiver VARCHAR(50), text VARCHAR(150))")
mysql_connection.commit()
cursor.close()


class Message(BaseModel):
    sender: str
    receiver: str
    text: str


def save_message_to_mysql(message: Message):
    cursor = mysql_connection.cursor()
    logging.info("init saving to mysql")
    cursor.execute(
        "INSERT INTO messages (sender, receiver, text) VALUES (%s, %s, %s)",
        (message.sender, message.receiver, message.text)
    )
    mysql_connection.commit()
    cursor.close()


def send_message(websocket, message: Message):
    message_dict = message.dict()
    websocket.send_json(message_dict)
    save_message_to_mysql(message)


connected_clients = []


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    logging.info("ws accepted, user_id=" + user_id)
    connected_clients.append(websocket)
    logging.info(connected_clients)

    messages = get_messages(user_id)
    for message in messages:
        await websocket.send_json(message)
        logging.info(message)

    while True:
        data = await websocket.receive_text()
        message = Message(**json.loads(data))
        send_message(websocket, message)

        for client in connected_clients:
            if client != websocket:
                await client.send_json(message)


def get_messages(user_id: str):
    logging.info('getting messages...')
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT * FROM messages WHERE ((receiver = %s) OR (sender = %s))", (user_id, user_id))
    messages = cursor.fetchall()
    cursor.close()
    return messages


html_content = """
<!DOCTYPE html> 
<html>
<head>
    <title>WebSocket Chat</title>
</head>
<body>
    <div>
        <input type="text" id="receiver" placeholder="receiver ID" />
        <input type="text" id="message" placeholder="Type a message..." />
        <button onclick="sendMessage()">Send</button>
    </div>
    <ul id="chat"></ul>
    <div>
        <h2>Sent Messages:</h2>
        <ul id="sentMessages"></ul>
    </div>
    <div>
    <h2>Received Messages:</h2>
    <ul id="receivedMessages"></ul>
    </div>
    <script>
        var receivedMessages = document.getElementById("receivedMessages");
        var sentMessages = document.getElementById("sentMessages");

        var socket = new WebSocket("ws://localhost:5000/ws/{{ user_id }}");
        socket.onmessage = function(event) {
            var message = JSON.parse(event.data);
            if (message.receiver == "{{ user_id }}") {
                receivedMessages.innerHTML += "<li><strong>" + message.sender + ":</strong> " + message.text + "</li>";
            }
            if (message.sender == "{{ user_id }}") {
                sentMessages.innerHTML += "<li><strong>" + message.receiver + ":</strong> " + message.text + "</li>";
            }
        };

        function sendMessage() {
            var receiverInput = document.getElementById("receiver");
            var messageInput = document.getElementById("message");
            var receiver = receiverInput.value;
            var message = messageInput.value;
            if (receiver && message) {
                socket.send(JSON.stringify({ sender: "{{ user_id }}", receiver: receiver, text: message }));
                messageInput.value = "";
                receiverInput.value = "";
        
                var sentMessages = document.getElementById("sentMessages");
                sentMessages.innerHTML += "<li><strong>" + receiver + ":</strong> " + message + "</li>";
            }
        }
    </script>
</body>
</html>
"""

template = Template(html_content)


@app.get("/test_chat/{user_id}", response_class=HTMLResponse)
async def test_chat(user_id: str):
    return HTMLResponse(content=template.render(user_id=user_id))
