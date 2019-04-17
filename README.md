# task-6

* Установка зависимостей:

    `$ python -m venv .venv`

    `$ source .venv/bin/activate`

    `$ pip instal --requirement requirements.txt`

* Установка базы данных из докера

    `$ docker-compose up -d`
    `$ docker exec -it task6 psql -U postgres -c "create database task6"`
* Запуск сервера:
 
    `FLASK_ENV=development FLASK_APP=wsgi flask run`
    
* Запуск тестов

    `python -m pytest tests/`
    
    
