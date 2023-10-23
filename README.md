# Foodgram
[Сслыка на сайт](https://new-foodgram.serveblog.net/)
---
## 1. Описание

Сервис "Продуктовый помощник" (Foodgram) предоставляет следующие возможности пользователям:

-Регистрация.

-Создание, изменение и удаление рецептов (есть база данных с подготовленными ингредиетами для них).

-Просмотр рецептов, опубликованных другими пользователями.

-Добавление рецептов других пользователей в избранное и корзину, а также скачивание списка ингердиентов для всех добавленных рецептов в виде csv файла.

-Подписка на других пользователей.

---
## 2. Заполнение базы данных и переменных окружения

Здесь используется база данных PostgreSQL.  
Для правильной настройки проекта и базы данных для него нужно создать и заполнить файл ".env" с переменными окружения в папке "./infra/".

Шаблон файла ".env":
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ'
ALLOWED_HOSTS='имя домена или ip хоста'
DEBUG=False
```

---
## 3. Запуск проекта

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/MuKeLaNGlo/foodgram-project-react.git
```

Запускаем контейнеры.  
Из папки "./infra/" выполнить команду:
```bash
sudo docker-compose up -d
```

После запуска контейнеров выполнить миграции:
```bash
sudo docker-compose exec backend python manage.py migrate
```

Создать суперпользователя:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

Собрать статику:
```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Теперь проект можно проверить по адресу [http://localhost/](http://localhost/)

---
## 4. Заполнение базы данных

Также есть заготовленные ингредиенты для рецептов, их можно импортировать.  
Заполнить базу данных ингредиентами можно выполнив следующую команду из папки "./infra/":
```bash
sudo docker-compose exec backend python manage.py load_data
```
Заполнить базу данных ингредиентами можно выполнив следующую команду из папки "./infra/":
```bash
sudo docker-compose exec backend python manage.py create_tags
```

---
## О проекте

Стек технологий: Python 3, Django, Django Rest, React, Docker, PostgreSQL, nginx, gunicorn, Djoser.

Веб-сервер: Nginx                 
Frontend: React                 
Backend: Django                
API: Django REST               
База данных: PostgreSQL
