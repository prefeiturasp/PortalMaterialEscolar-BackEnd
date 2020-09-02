#FROM python:3.6-jessie
FROM python:3.6-buster
ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
RUN apt-get update && apt-get install && \
    python -m pip --no-cache install -U pip && \
  #    python -m pip --no-cache install Cython && \
  #    python -m pip --no-cache install numpy && \
  python -m pip --no-cache install -r requirements/production.txt


EXPOSE 8001
