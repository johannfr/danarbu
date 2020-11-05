FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash build-base mariadb-connector-c-dev
ENV STATIC_URL /static
ENV STATIC_PATH /app/danarbu/static
ENV TZ Atlantic/Reykjavik
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /var/www/requirements.txt
