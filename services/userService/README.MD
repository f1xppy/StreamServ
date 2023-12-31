# API чат-сервиса


# Зависимости

Перед запуском сервиса необходимо установить зависимости из файла requirements.txt

# Запуск

```bash
uvicorn app:app --port 5000 --reload
```

# Запуск с использование файла конфигурации .env

Для запуска из файла конфигурации нужно поместить файл .env в корень сервиса

# Конфигурация
| Переменная                                            | Назначение                                                         | Значение по-умолчанию                  |
|-------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------|
| MYSQL_DSN                                             | Строка подключения к MYSQL                                         | mysql+asyncmy://user:pass@localhost/db |
| JWT_SECRET                                            | Парольная фраза, используемая для кодирования jwt-токена           | jwt_secret                             | 
| RESET_PASSWORD_TOKEN_SECRET                           | Парольная фраза, используемая для кодирования токена сброса пароля | reset_password_token_secret            | 
| VERIFICATION_TOKEN_SECRET                             | Парольная фраза, используемая для кодирования токена верификации   | verification_token_secret              | 
| MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER  | Данные для авторизации в почтовой системе для подключения мейлера  |                                        | 

# Документация

После запуска доступна документация: http://127.0.0.1:5000/docs


# Сборка образа
```bash
docker build -t streamserv/userservice:0.0.2 .
```