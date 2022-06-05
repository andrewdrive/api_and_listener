# API_and_listener
two_services
## Add your files
```
cd existing_repo
git remote add origin https://gitlab.com/andrewdrive/api_and_listener.git
git branch -M main
git push -uf origin main
```
## Installation
    $ docker-compose up
    $ docker-compose exec api bash
    $ python manage.py createsuperuser
username: admin
password: admin (т.к. захардкожено)

## Usage
    http://localhost:8001/swagger

## Test and Deploy
    http://localhost:8001/api/v1/message/

    request body = {
        "user_id": 1,
        "text": "абракадабра"
    }

## Description
Клиент отправляет сообщение в API сервис.
Сервис сохраняет сообщение в БД со статусом "на проверке". В БД сообщение может находится в трёх состояниях: на проверке, заблокировано, корректно (review, blocked, correct).
Сервис кладёт сообщение в кафку, которую читает листенер.
Листенер проверяет, что в тексте сообщения не встречается слово "АБРАКАДАБРА" (в любом регистре).
После того, как листенер проверит сообщение, он отправляет в API сервис статус проверки (true/false).
API сервис изменяет статус сообщения. Если сообщение корректно, для него устанавливается статус "корректно", иначе - "заблокировано".

## Authors and acknowledgment
andrewdrive
