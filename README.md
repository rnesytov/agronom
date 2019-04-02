# Agronom

# Установка
## Бэкенд
```
virtualenv myvenv
source myvenv/bin/activate
cd agronom
pip install -r requirements.txt
```
## Фронтенд
Установить [yarn](https://yarnpkg.com/en/docs/install)
```
cd agronom/frontend
yarn
```
## БД
```
CREATE DATABASE agronom_db;
CREATE USER test_agronom_user WITH ENCRYPTED PASSWORD 'pass';
GRANT ALL privileges ON DATABASE agronom_db TO test_agronom_user;
\c agronom_db
CREATE EXTENSION postgis;
```

# Запуск
## Django сервер
```
cd agronom
./manage.py runserver
```
## Celery
```
cd agronom
celery -A agronom worker
```

## Фронтенд сервер
```
cd agronom/frontend
yarn start
```


# Тесты
```
cd agronom
./manage.py test
```
