import pymysql.cursors
from app.schemas.models import Message

mysql_connection = pymysql.connect(
    host="localhost",
    user="streamserv",
    password="streamserv",
    database="streamserv",
    cursorclass=pymysql.cursors.DictCursor
)


def create_table():
    cursor = mysql_connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS messages (id int(10) AUTO_INCREMENT PRIMARY KEY, sender VARCHAR(50), receiver VARCHAR(50), text VARCHAR(150))")
    mysql_connection.commit()
    cursor.close()


def save_message_to_mysql(message: Message):
    cursor = mysql_connection.cursor()
    cursor.execute(
        "INSERT INTO messages (sender, receiver, text) VALUES (%s, %s, %s)",
        (message.sender, message.receiver, message.text)
    )
    mysql_connection.commit()
    cursor.close()