FROM python:3

ENV PYTHONUNBUFFORED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install --no-cache-dir -r requirements.txt
