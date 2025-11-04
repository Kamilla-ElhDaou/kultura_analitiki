Приложение для тестового задания на позицию Junior-разработчик SaaS-сервиса «Культура аналитики»

Demo реализовано с использованием aiohttp, sqlalchemy, asyncpg.<br>
Автоматическая генерация контрактов OpenAPI с помощью aiohttp_swagger3.<br>
Приложение будет достпуно по http://127.0.0.1:8080<br>
Документация доступна по http://127.0.0.1:8080/docs<br>
Для создание Postgres DB в контейнере Docker.

```
docker run --name pg_demo -e POSTGRES_DB=postgres -e POSTGRES_USER=init_user -e POSTGRES_PASSWORD=init_secret_password -p 5432:5432 -d postgres:16
```
Создание базы данных и наполнение тестовыми данными.
```
python init_db.py
```
Запуск тестов.
```
pytest
```
Запуск приложения.
```
python -m application --host=127.0.0.1 --port=8080
```
Генератция клиент из контрактов.
```
openapi-generator-cli generate -i http://127.0.0.1:8080/docs/swagger.json -g python-aiohttp -o ./client
```
