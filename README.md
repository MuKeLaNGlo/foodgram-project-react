# Foodgram
[Сслыка на сайт](https://new-foodgram.serveblog.net/)
---
## 1. Описание

Сервис "Продуктовый помощник" (Foodgram) предоставляет следующие возможности пользователям:

  -Регистрация в системе.
  -Создание собственных рецептов с возможностью управления ими (редактирование, удаление).
  -Просмотр рецептов, опубликованных другими пользователями.
  -Добавление рецептов других пользователей в избранное и корзину.
  -Подписка на активность других пользователей.
  -Возможность скачать список ингредиентов для рецептов, добавленных в корзину.

---
## 2. Заполнение базы данных и переменных окружения

Проект использует базу данных PostgreSQL.  
Для подключения и выполненя запросов к базе данных необходимо создать и заполнить файл ".env" с переменными окружения в папке "./infra/".

Шаблон для заполнения файла ".env":
```python
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY='секретный ключ'
ALLOWED_HOSTS='имя домена или ip хоста'
```

---
## 3. Команды для запуска

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/MuKeLaNGlo/foodgram-project-react.git
```

Запустить контейнеры.  
Из папки "./infra/" выполнить команду:
```bash
docker-compose up -d
```

После успешного запуска контейнеров выполнить миграции:
```bash
sudo docker-compose exec backend python manage.py migrate
```

Создать суперюзера (Администратора):
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

С проектом поставляются данные об ингредиентах.  
Заполнить базу данных ингредиентами можно выполнив следующую команду из папки "./infra/":
```bash
sudo docker-compose exec backend python manage.py load_data
sudo docker-compose exec backend python manage.py create_tags
```

---
## 5. Техническая информация

Стек технологий: Python 3, Django, Django Rest, React, Docker, PostgreSQL, nginx, gunicorn, Djoser.

Веб-сервер: Nginx                 
Frontend: React                 
Backend: Django                
API: Django REST               
База данных: PostgreSQL
