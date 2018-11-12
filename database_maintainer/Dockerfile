FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /btc-blocks-data/
EXPOSE 27017
CMD [ "python", "-u", "/src/update_database.py" ]
