import pymysql.cursors
from app.schemas.models import Message
from . import config


cfg: config.Config = config.load_config()

mysql_connection = pymysql.connect(
    host=cfg.mysql_host,
    user=cfg.mysql_user,
    password=cfg.mysql_password,
    database=cfg.mysql_database,
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
