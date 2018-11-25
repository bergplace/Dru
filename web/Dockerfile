FROM python:3.7

COPY requirements.txt ./

RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

#RUN python manage.py migrate

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]