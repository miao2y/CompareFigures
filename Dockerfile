FROM python:3.11

# install
WORKDIR src
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./ .
#
#RUN cat requirements.txt
#
ENTRYPOINT ["flask","--app","api","run","--port","7777", "--host","0.0.0.0"]