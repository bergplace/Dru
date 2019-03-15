FROM debian:buster
RUN apt-get update && \
    apt-get install -y apt-transport-https wget gnupg2 && \
    wget -qO - https://apt.z.cash/zcash.asc | apt-key add - && \
    echo "deb [arch=amd64] https://apt.z.cash/ jessie main" | tee /etc/apt/sources.list.d/zcash.list && \
    apt-get update && apt-get install -y zcash && \
    zcash-fetch-params

RUN apt-get install -y gettext-base htop nano

COPY .zcash /root/.zcash
COPY start.sh /root/start.sh
COPY zcash.conf /root/template.zcash.conf
EXPOSE 8232
WORKDIR /root
CMD bash /root/start.sh
