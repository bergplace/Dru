FROM python:3

COPY requirements.txt ./
COPY data_load_progress_tracker.py ./
COPY ./src/ /src/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install https://github.com/alecalve/python-bitcoin-blockchain-parser/archive/master.zip
RUN mkdir /btc-blocks-data/

EXPOSE 27017

CMD [ "python", "-u", "/src/update_database.py" ]
