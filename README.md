# Тестовое задание
```
стек:
django
rest framework
celery
redis
```

## Установка и запуск

1. Склонировать репозиторий с Github:
```
git clone https://github.com/Alexandr-Well/Newsletter.git
```

2. В дирректории проекта создать виртуальное окружение с учетом вашей ОС:

```
python -m venv venv
```
SECRET_KEY
3. В файле .evn заполнить необходимые данные:
```
SECRET_KEY - ключь проекта Django
TOKEN - токен для стороннпего API
```

4. Установка зависимостей:
```
pip install -r requirements.txt
```

5. Создать и применить миграции в базу данных:
```
python manage.py makemigrations
python manage.py migrate
```
6. Запустить сервер
```
для каждой команды в отдельном терменале
python manage.py runserver
docker run -p 127.0.0.1:6379:6379 redis:latest
celery -A app_mail worker -l info -P eventlet
celery -A app_mail flower --port=5555 -n flower
celery -A app_mail beat -l info -P eventlet
```

***
## URLS
***
```
http://0.0.0.0:8000/docs/
http://0.0.0.0:8000/api/clients/
http://0.0.0.0:8000/api/newsletter/
http://0.0.0.0:8000/api/newsletter/newsletter_info/
http://0.0.0.0:8000/api/newsletter/<pk>/message_info/
http://0.0.0.0:8000/api/messages/
```
***
## Выполненные дополнительные задания:
```п. 5```
```п. 8```
```п. 9```
***
## Пункты которые хотел бы выполнить, но не успел:
```п. 1```
```п. 3```
```п. 10```
```п. 12```
## Примечания
1. приложение send_email_app пока не в работе планируется под рассылку почты клиентам
## TODO
***
1. доработать docker-compose.yml - сейчас есть проблема с запуском серверов, проблема маршрутизации
2. написать тесты
***
