FROM python:3

COPY requirements.txt ./
COPY ./src/ /src/
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir /btc-blocks-data/

CMD [ "python", "/src/update_database.py" ]
