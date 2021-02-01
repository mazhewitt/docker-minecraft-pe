FROM python:slim-buster

ARG ARCH=amd64
EXPOSE 19132/udp
VOLUME /mc-data

RUN ["mkdir", "/opt/server"]
RUN ["mkdir", "/opt/server/downloads"]
COPY ["start_server.py", "/opt/server"]
RUN ["chmod", "755", "/opt/server/start_server.py"]

ENTRYPOINT /opt/server/start_server.py

