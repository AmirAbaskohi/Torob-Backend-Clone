FROM python:3

ENV PYTHONUNBUFFORED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/

COPY test.sh /test.sh
RUN chmod +x /test.sh

RUN pip install --no-cache-dir -r requirements.txt
