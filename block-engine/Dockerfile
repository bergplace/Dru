FROM python:3.7.1-stretch

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 27017
CMD [ "python", "-u", "/src/update_database.py" ]
