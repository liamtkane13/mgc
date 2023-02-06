FROM python:3.9

# To build:
# docker build -t liamtkane/seqfailr

RUN apt-get update
RUN apt-get install -y pip git vim 
RUN pip install numpy matplotlib seaborn
RUN cd /var/ && git clone https://github.com/cdelahaye/SeqFaiLR
RUN cd /var/SeqFaiLR/ && ./seqfailr --init
COPY D1_Direct_Aspergillus_Reads_samestrand.fasta /var/SeqFaiLR/Data/ 
COPY A_niger_Rockefeller_Amplicon.fasta /var/SeqFaiLR/Data/ 