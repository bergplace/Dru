FROM python:3

COPY requirements.txt ./
COPY ./src/ /src/
RUN pip install --no-cache-dir -r requirements.txt

# newest version
#RUN pip install https://github.com/alecalve/python-bitcoin-blockchain-parser/archive/master.zip

# forked version from 22.03.2018
RUN pip install https://github.com/MarcinPieczka/python-bitcoin-blockchain-parser/archive/master.zip

RUN mkdir /btc-blocks-data/

EXPOSE 27017

CMD [ "python", "-u", "/src/update_database.py" ]
