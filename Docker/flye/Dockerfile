FROM ubuntu:latest

# To build:
# docker build -t liamtkane/flye .

RUN apt-get update
RUN apt-get install -y python3 git pip
RUN pip install setuptools
RUN git clone https://github.com/fenderglass/Flye
RUN cd Flye/ && python3 setup.py install
