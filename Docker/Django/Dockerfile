FROM ubuntu:latest

# To build:
# docker build -t liamtkane/django .

RUN apt-get -y update
RUN apt-get install -y python3.9 pip vim default-libmysqlclient-dev build-essential 
RUN cd opt/ && pip install Django
RUN cd opt/ && apt-get install -y mysql-server
RUN touch /var/run/mysqld/mysqld.sock && chown mysql /var/run/mysqld/mysqld.sock
RUN pip install mysqlclient
