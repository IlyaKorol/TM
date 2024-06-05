# Task Manager

## Описание проекта

Task Manager - это веб-приложение для управления задачами. Пользователи могут создавать, редактировать, удалять задачи, а также отмечать их как выполненные и добавлять в избранное.

## Технологии

- Python

- Django

- Django REST Framework

- Gunicorn

- Nginx

## Установка и запуск

### Установка

1. Клонируйте репозиторий на свой компьютер:

```git clone https://github.com/IlyaKorol/diploma```

2. Перейдите в директорию проекта:

```cd task_manager```

3. Установите виртуальное окружение:


```python -m venv venv```

4. Активируйте виртуальное окружение:

- На Windows:

```venv\Scripts\activate```

- На macOS/Linux:

```source venv/bin/activate```

5. Установите зависимости:

```pip install -r requirements.txt```

6. Настройте базу данных в файле settings.py.

7. Примените миграции:

```python manage.py migrate```

8. Создайте суперпользователя:

```python manage.py createsuperuser```

### Запуск

1. Запустите локальный сервер разработки Django:

```python manage.py runserver```

2. Откройте браузер и перейдите по адресу http://127.0.0.1:8000/.

## API

### Получение списка задач

- URL: /api/tasks/

- Метод: GET

- Описание: Возвращает список всех задач.

Формат ответа:

```
[
  {
    "id": 1,
    "title": "Название задачи",
    "description": "Описание задачи",
    "priority": 1,
    "due_date": "2024-12-31",
    "completed": false,
    "user": 1,
    "created_at": "2024-06-05T12:00:00Z"
  },
  ...
]
```

Создание новой задачи

- URL: /api/tasks/

- Метод: POST

- Описание: Создает новую задачу.

Параметры запроса:

- title (обязательно): Название задачи.

- description (опционально): Описание задачи.

- priority (обязательно): Приоритет задачи (1 - Low, 2 - Medium, 3 - High).

- due_date (обязательно): Дата завершения задачи (формат YYYY-MM-DD).

- completed (опционально): Статус выполнения задачи (по умолчанию false).

Пример запроса:

```
{
  "title": "Новая задача",
  "description": "Описание новой задачи",
  "priority": 2,
  "due_date": "2024-12-31",
  "completed": false
}
```

Формат ответа:

```
{
  "id": 1,
  "title": "Новая задача",
  "description": "Описание новой задачи",
  "priority": 2,
  "due_date": "2024-12-31",
  "completed": false,
  "user": 1,
  "created_at": "2024-06-05T12:00:00Z"
}
```

Обновление задачи

- URL: ```/api/tasks/<id>/```

- Метод: PUT

- Описание: Обновляет задачу по ее ID.

Параметры запроса: Такие же, как и для создания новой задачи.

Удаление задачи

- URL: ```/api/tasks/<id>/```

- Метод: DELETE

- Описание: Удаляет задачу по ее ID.

Получение списка избранных задач

- URL: ```/api/favorite-tasks/```

- Метод: GET

- Описание: Возвращает список всех избранных задач.

Формат ответа:

```
[
  {
    "id": 1,
    "user": 1,
    "task": 1
  },
  ...
]
```

## Развертывание на хостинге

### Установка Gunicorn и Nginx

1. Установите Gunicorn:

```pip install gunicorn```

2. Установите Nginx. На Ubuntu это можно сделать так:

```sudo apt update```

```sudo apt install nginx```

### Настройка Gunicorn

1. Создайте файл gunicorn.service в /etc/systemd/system/ со следующим содержимым:

```
[Unit]

Description=gunicorn daemon

After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/your/venv/bin/gunicorn --workers 3 --bind unix:/path/to/your/project.sock task_manager.wsgi:application

[Install]
WantedBy=multi-user.target
```

2. Запустите и включите службу Gunicorn:

```sudo systemctl start gunicorn```

```sudo systemctl enable gunicorn```

### Настройка Nginx

1. Создайте конфигурационный файл для вашего сайта в /etc/nginx/sites-available/:

```
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/path/to/your/project.sock;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

2. Создайте символическую ссылку в /etc/nginx/sites-enabled/:

```sudo ln -s /etc/nginx/sites-available/your_site /etc/nginx/sites-enabled```

3. Перезапустите Nginx:

```sudo systemctl restart nginx```

## Инструкция пользователя

### Создание новой задачи

1. Перейдите на страницу "Создать задачу".

2. Заполните форму создания задачи, указав название, описание и другие необходимые данные.

3. Нажмите кнопку "Создать", чтобы сохранить задачу.

### Просмотр и редактирование задачи

1. На главной странице отображается список всех задач.

2. Чтобы просмотреть подробную информацию о задаче, нажмите на ее название.

3. Для редактирования задачи нажмите кнопку "Изменить" на странице просмотра задачи.

### Удаление задачи

1. Для удаления задачи перейдите на страницу просмотра задачи.

2. Нажмите кнопку "Удалить".

3. Подтвердите удаление, если система запросит подтверждение.

### Управление избранными задачами
1. Чтобы добавить задачу в избранное, нажмите кнопку "Добавить в избранное" на странице просмотра задачи.

2. Чтобы удалить задачу из избранного, нажмите кнопку "Удалить из избранного" на странице просмотра задачи.

## Дополнительная информация

Если у вас есть вопросы или предложения, вы можете связаться с разработчиком по email: ```ilyakorol94@gmail.com.```