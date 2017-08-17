FROM python:3.6
MAINTAINER Kosenko Artyom <kosc@hotkosc.ru>
COPY requirements.txt /usr/src/
WORKDIR /usr/src
RUN pip install -r requirements.txt
