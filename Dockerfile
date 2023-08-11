FROM python:3.10-alpine

RUN adduser -D memateka

WORKDIR /home/memateka

COPY requirements.txt requirements.txt
RUN install -r requirements.txt
RUN install gunicorn

COPY app app
COPY migrations migrations
COPY main.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R memateka:memateka ./
USER memateka

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]