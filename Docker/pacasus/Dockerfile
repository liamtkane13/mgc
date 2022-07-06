FROM ubuntu:latest

# To build:
# docker build -t liamtkane/pacasus .

RUN apt-get update
RUN apt-get install -y python3 git pip
RUN pip install setuptools
RUN git clone https://github.com/swarris/Pacasus.git
RUN pip install numpy && pip install Biopython
RUN cd Pacasus/ && git submodule init && git submodule update
