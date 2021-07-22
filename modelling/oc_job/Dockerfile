FROM docker-remote.artifacts.developer.gov.bc.ca/osgeo/gdal:ubuntu-small-latest

WORKDIR /dataload

COPY ./script/scrape_stations.py /dataload/

RUN useradd wally -M -G root -u 1021 && chmod -R 775 /dataload \
  && chown -R wally:root /dataload \
  && apt-get update && apt-get install -y \
    jq curl git zip unzip binutils libproj-dev python3 python3-pip \
    build-essential zlib1g-dev sbcl make gawk freetds-dev libzip-dev \
    gfortran make gcc g++ curl libssl-dev libcurl4-openssl-dev \
    r-base r-base-dev r-base-core r-recommended \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install requests matplotlib numpy pandas minio \
  && Rscript -e 'install.packages("Rcpp", repos="https://cloud.r-project.org")' \
  && Rscript -e 'install.packages("fasstr", repos="https://cloud.r-project.org")' \
  && mkdir -p ~/.local/share/tidyhydat

RUN curl https://collaboration.cmc.ec.gc.ca/cmc/hydrometrics/www/Hydat_sqlite3_20210510.zip -o Hydat.zip && unzip Hydat.zip \
&& mv ./Hydat.sqlite3 ~/.local/share/tidyhydat/ \
&& touch ~/.local/share/tidyhydat/HYDAT.sqlite3

USER 1021
CMD ["python3", "/dataload/scrape_stations.py"]
