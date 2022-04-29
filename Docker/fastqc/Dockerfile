FROM openjdk:11-slim

#To build:
#docker build -t liamtkane/fastqc .

RUN apt-get update 
RUN apt-get install -y wget unzip libfreetype6-dev cpanminus

RUN cd /opt/ && \
    wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip
RUN cd /opt/ && \
    unzip fastqc_v0.11.9.zip
RUN chmod u+x /opt/FastQC/fastqc
#COPY P.Cubensis_0.5.R1.fastq /opt/P.Cubensis_0.5.R1.fastq
