FROM docker-remote.artifacts.developer.gov.bc.ca/osgeo/gdal:ubuntu-small-latest

WORKDIR /dataload

COPY ./script/scrape_stations.py /dataload/

RUN useradd wally -M -G root -u 1021 && chmod -R 775 /dataload \
  && chown -R wally:root /dataload \
  && apt-get update && apt-get install -y jq curl git zip unzip binutils libproj-dev python3 python3-pip \
                                          build-essential zlib1g-dev \
                                          sbcl make gawk freetds-dev libzip-dev \
  && rm -rf /var/lib/apt/lists/* \
  && pip3 install requests matplotlib numpy pandas minio

USER 1021
CMD ["python3", "/dataload/scrape_stations.py"]
