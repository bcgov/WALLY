FROM crunchydata/crunchy-postgres-gis:centos8-13.2-3.0-4.6.2

USER root

RUN dnf --disablerepo=crunchypg13 install -y epel-release dnf-plugins-core && dnf config-manager --set-enabled powertools && \
yum -y --disablerepo=crunchypg13 install gcc-gfortran make gcc gcc-c++ libcurl-devel libxml2-devel openssl-devel texlive-* R-devel && \
Rscript -e 'install.packages("fasstr", repos="https://cloud.r-project.org")'

USER postgres
