FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py collectstatic --no-input
RUN python manage.py create_tags
RUN python manage.py load_data

CMD ["gunicorn", "--bind", "0:8000", "foodgram.wsgi:application"]