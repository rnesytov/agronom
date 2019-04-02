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
