FROM ubuntu:latest

# To build:
# docker build -t liamtkane/samtools .

RUN apt-get update
RUN apt-get install -y wget samtools
COPY sample.bam /opt/
