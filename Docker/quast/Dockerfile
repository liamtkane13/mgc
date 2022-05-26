FROM ubuntu:latest

# To build:
# docker build -t liamtkane/quast .

RUN apt-get update
RUN apt-get install -y python3 pip vim
RUN pip install quast
COPY jsontemplate.py /usr/local/lib/python3.10/dist-packages/quast_libs/site_packages/jsontemplate/
