FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY core ./core
COPY todolist_diplom ./todolist_diplom
COPY manage.py .
COPY .env .
CMD python manage.py runserver 0.0.0.0:8000
