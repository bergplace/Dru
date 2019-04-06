FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    python3-dev \
    supervisor \
    nginx

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r /requirements.txt

RUN useradd -ms /bin/bash www-user
RUN mkdir -p /var/log/uwsgi

COPY conf/uwsgi.ini /home/www-user/
COPY conf/supervisord.conf /home/www-user/
COPY conf/web /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/web /etc/nginx/sites-enabled/

WORKDIR /app

# Server
EXPOSE 80
STOPSIGNAL SIGINT
CMD ["bash", "start.sh"]