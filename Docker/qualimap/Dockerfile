FROM ubuntu:latest

# To build:
# docker build -t liamtkane/qualimap .

RUN apt-get update

RUN apt-get install -y wget openjdk-8-jre
RUN apt-get install -y r-base r-base-dev

RUN apt-get install -y software-properties-common build-essential \
	wget libcurl4-openssl-dev libxml2-dev libssl-dev unzip littler

RUN rm -rf /var/lib/apt/lists/*
RUN Rscript -e "install.packages('optparse')"
RUN Rscript -e "install.packages('BiocManager', repos = 'http://cran.us.r-project.org')"
RUN Rscript -e "BiocManager::install(c('NOISeq', 'Repitools'))"
RUN cd /opt && wget https://bitbucket.org/kokonech/qualimap/downloads/qualimap-build-31-08-20.tar.gz
#RUN cd /opt && unzip qualimap_v2.2.1.zip && rm qualimap_v2.2.1.zip
#RUN Rscript /opt/qualimap_v2.2.1/scripts/installDependencies.r

#ENV PATH="/opt/qualimap_v2.2.1:$PATH"
 
#COPY sample.bam /opt/
