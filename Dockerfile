FROM python:3

ENV PYTHONUNBUFFORED 1
ENV SUGGESTOIN_BASE_URL 'http://127.0.0.1:8010/'
RUN mkdir /code
WORKDIR /code
COPY . /code/

COPY test.sh /test.sh
RUN chmod +x /test.sh

RUN pip install --no-cache-dir -r requirements.txt
