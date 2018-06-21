FROM beakerx/beakerx

MAINTAINER Mutlu Polatcan <mutlupolatcan@gmail.com>

USER root

RUN conda install -n beakerx pystan && \
    conda install -n beakerx -c conda-forge fbprophet && \
    conda install -n beakerx -c conda-forge scikit-learn && \
    conda install -n beakerx -c conda-forge scipy && \
    conda install -n beakerx -c conda-forge jupyterthemes
