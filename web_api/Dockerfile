FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt /
COPY custom.conf /etc/nginx/conf.d/

RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app
