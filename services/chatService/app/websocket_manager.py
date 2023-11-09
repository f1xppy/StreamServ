from .models import Message
from .database import save_message_to_mysql, mysql_connection


def send_message(websocket, message: Message):
    message_dict = message.dict()
    websocket.send_json(message_dict)
    save_message_to_mysql(message)


def get_messages(user_id: str):
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT * FROM messages WHERE ((receiver = %s) OR (sender = %s))", (user_id, user_id))
    messages = cursor.fetchall()
    cursor.close()
    return messages

