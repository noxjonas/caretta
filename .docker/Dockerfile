FROM ubuntu:18.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN conda --version

RUN conda install python
RUN conda install -c bioconda msms
RUN conda install -c salilab dssp
RUN conda install git
RUN pip install --upgrade pip setuptools wheel

RUN apt-get update
RUN apt-get install build-essential -y
RUN gcc --version

COPY . .

RUN pip install -e ".[GUI]"

EXPOSE 8091
