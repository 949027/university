# Сервис для организации учебного процесса в ВУЗе
Бэкенд — Django + DRF.  
БД — Postgres.  
Очередь заданий — Celery.  
Брокер/бэкенд — Redis.

## Перед запуском
1) Скачайте проект:
```commandline
git clone https://github.com/949027/university
```
2) Создайте файл `.env` в корне проекта со следующими настройками.

Необходимо:
- `SECRET_KEY` — [секретный ключ](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) проекта. Он отвечает за шифрование на сайте.

Необязательно:
- `DEBUG` - [дебаг-режим](https://docs.djangoproject.com/en/4.1/ref/settings/#debug). По умолчанию - True.
- `ALLOWED_HOSTS` - [список допустимых хостов](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts). По умолчанию - 127.0.0.1, localhost.
- `DB_URL` - конфигурация БД, указывается в [виде URL](https://github.com/jazzband/dj-database-url). Например `postgres://test_user:test_password@localhost:5432/test_db` (для запуска в Docker используйте `db` вместо `localhost`). Если значение не указано, то используется SQLite, имя файла `db.sqlite3`.
- `MAX_GROUP_SIZE` - максимальное количество учеников группе. По умолчанию - 20.

## Запуск в Docker
1) Установите [Docker](https://docs.docker.com/engine/install/) и [Docker Compose](https://docs.docker.com/compose/install/).
2) Соберите и запустите контейнеры:
```commandline
docker-compose up
```
3) В другом терминале создайте суперпользователя:
```commandline
docker exec -it web python manage.py createsuperuser
```

## Запуск на локальной машине 
1) [Python3](https://www.python.org/downloads/) должен быть уже установлен.
2) Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html) для изоляции проекта.
3) Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```commandline
pip install -r requirements.txt
```
4) Настройте Postgres ([пример](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart-ru)) или не указывайте переменную окружения `DB_URL`, тогда будет использоваться SQLite. 
5) Настройте [Redis](https://redis.io/docs/getting-started/).
6) Проведите миграции БД:
```commandline
python manage.py migrate
```
7) Создайте суперпользователя:
```commandline
python manage.py createsuperuser
```
8) В отдельном терминале запустите Celery:
```commandline
celery -A university worker -l info
```
9) В отдельном терминале запустите Flower (мониторинг задач Celery):
```commandline
celery -A university flower --port=5555 --broker=redis://redis:6379/0
```
Панель будет доступна по адресу http://127.0.0.1:5555
10) Запустите разработческий сервер ([не годится для production](https://docs.djangoproject.com/en/4.1/ref/django-admin/#runserver)):
```commandline
python manage.py runserver
```

## Как использовать
### Админ-панель
Админ-панель доступна по адресу http://127.0.0.1:8000/admin. 

### Токен для авторизации
Отправить post-запрос на http://127.0.0.1:8000/api/v1/token/ с `username` и `password` пользователя в теле запроса.
```commandline
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://127.0.0.1:8000/api/v1/token/
```
Полученный токен необходимо указывать с префиксом `Token` в заголовке `Authorization` каждого запроса, например:
```commandline
curl -X GET -H "Authorization: Token d6e8ab88abac0d08a74fd235bcd99bfe4c1eb5cb" http://127.0.0.1:8000/api/v1/student/
```

### Функционал куратора и администратора

| Конечная точка                                | Объект               | HTTP-методы             | Куратор | Администратор |
|-----------------------------------------------|----------------------|-------------------------|---------|---------------|
| /api/v1/student/                              | список студентов     | GET, POST               | +       | +             |
| /api/v1/student/{student_id}                  | студент              | GET, PUT, PATCH, DELETE | +       | +             |
| /api/v1/group/                                | список групп         | GET, POST               | +       | +             |
| /api/v1/group/{group_id}                      | группа               | GET, PUT, PATCH, DELETE | +       | +             |
| /api/v1/course                                | список направлений   | GET, POST               | -       | +             |
| /api/v1/course/{course_id}                    | направление          | GET, PUT, PATCH, DELETE | -       | +             |
| /api/v1/subject                               | список дисциплин     | GET, POST               | -       | +             |
| /api/v1/subject/{subject_id}                  | дисциплина           | GET, PUT, PATCH, DELETE | -       | +             |
| /api/v1/create-report/                        | id задачи Celery     | GET                     | -       | +             |
| /api/v1/create-report/status-report/{task_id} | статус задачи Celery | GET                     | -       | +             |
| /api/v1/create-report/get-report/             | отчёт (report.xlsx)  | GET                     | -       | +             |

## Цели проекта
Код написан в качестве тестового задания.