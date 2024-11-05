FROM python:slim-bookworm

ARG ARCH=amd64
EXPOSE 19132/udp
VOLUME /mc-data

RUN apt-get update && apt-get install -y curl cron && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/server
RUN mkdir /opt/server/downloads
COPY start_server.py /opt/server/start_server.py
COPY mc_setup.py /opt/server/mc_setup.py
COPY backup-minecraft.py /opt/server/backup-minecraft.py
COPY version.sh /opt/server/version.sh
COPY requirements.txt /opt/server/requirements.txt

RUN pip install -r /opt/server/requirements.txt

RUN chmod 755 /opt/server/start_server.py
RUN chmod 755 /opt/server/backup-minecraft.py
RUN chmod 755 /opt/server/version.sh

COPY backup-crontab /etc/cron.d/backup-crontab
RUN crontab /etc/cron.d/backup-crontab

WORKDIR /opt/server/

ENTRYPOINT ["/usr/local/bin/python", "/opt/server/start_server.py"]