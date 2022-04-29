FROM ubuntu:latest

# To build:
# docker build -t liamtkane/multiqc .

RUN apt-get update
RUN apt-get install -y python3 pip
RUN cd opt/ && pip install multiqc
