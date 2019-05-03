FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    python3-dev \
    supervisor \
    nginx \
    libpcre3 libpcre3-dev pkg-config libxml2 libxml2-dev zlib1g-dev

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r /requirements.txt

RUN mkdir -p /srv/conf
RUN mkdir -p /srv/log
RUN mkdir -p /srv/static

COPY conf/uwsgi.ini /srv/conf
COPY conf/supervisord.conf /srv/conf
COPY conf/web-tls-off /etc/nginx/sites-available/
COPY conf/web-tls-on /etc/nginx/sites-available/
RUN rm /etc/nginx/sites-enabled/default


RUN chown -R www-data /srv
RUN chown -R www-data /etc/nginx

WORKDIR /app

# Server
EXPOSE 80
STOPSIGNAL SIGINT
CMD ["bash", "start.sh"]