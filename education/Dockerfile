FROM python:3
LABEL maintainer="nyuskov@gmail.com"
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt --root-user-action ignore

