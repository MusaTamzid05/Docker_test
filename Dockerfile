FROM python:3.5


RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask uWSGI requests
WORKDIR /app
COPY app /app
COPY cmd.sh /


EXPOSE 9090 9191
USER uwsgi

CMD [ "/cmd.sh"]


