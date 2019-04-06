FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    build-essential \
    python3-dev \
    supervisor

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r /requirements.txt

RUN useradd -ms /bin/bash www-user
RUN mkdir -p /var/log/uwsgi

COPY conf/ /home/www-user/

WORKDIR /app

# Server
EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["bash", "start.sh"]