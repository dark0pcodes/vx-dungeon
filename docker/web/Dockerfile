FROM python:3.6-buster

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install libfuzzy-dev

WORKDIR /opt/vx-dungeon
RUN mkdir src
COPY src /opt/vx-dungeon/src

RUN mkdir config
COPY config /opt/vx-dungeon/config

WORKDIR /opt/vx-dungeon/src
RUN pip install --upgrade pip
RUN pip install -r web/requirements.txt

RUN python -m unittest discover -s web/tests

ENTRYPOINT ["python", "wsgi.py"]