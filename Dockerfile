FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE='app.settings'

RUN python app/manage.py migrate

CMD ["python", "app/app/manage.py", "runserver", "0.0.0.0:8000"]