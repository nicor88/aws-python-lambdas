FROM scratch
ADD amzn-container-minimal-2017.03.0.20170401-x86_64.tar.xz /

RUN yum install -y bzip2 find unzip

ENV MINICONDA Miniconda3-latest-Linux-x86_64.sh
ENV MINICONDA_URL https://repo.continuum.io/miniconda/$MINICONDA
ENV CONDA_DIR /opt/miniconda

WORKDIR /tmp
RUN curl -L $MINICONDA_URL  -o miniconda.sh
RUN bash miniconda.sh -b -p $CONDA_DIR
RUN rm /tmp/miniconda.sh

# setup conda in the env
ENV PATH $CONDA_DIR/bin:$PATH

CMD ["/bin/bash"]
