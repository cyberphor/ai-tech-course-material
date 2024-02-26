# Dockerfile metadata
FROM python:3.9-alpine3.13 
LABEL Author="Victor Fernandez III, @cyberphor"

RUN pip install --upgrade pip setuptools wheel
RUN pip install Django djangorestframework djangorestframework-simplejwt[crypto] 

WORKDIR /opt/loginservice/
COPY django/task3/ task3/
COPY django/db.sqlite3 db.sqlite3
COPY django/manage.py manage.py

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]