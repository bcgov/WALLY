FROM docker-remote.artifacts.developer.gov.bc.ca/osgeo/gdal:ubuntu-small-latest

WORKDIR /dataload

COPY ./hydat/load_hydat.sh /dataload/
COPY ./databc/*.sh /dataload/
COPY ./prism/*.sh /dataload/
COPY ./cdem/*.sh /dataload/
COPY ./tiles/create_tileset.sh /dataload/
COPY ./tiles/upload_tileset.sh /dataload/

RUN useradd wally -M -G root -u 1021 && chmod -R 775 /dataload \
  && chown -R wally:root /dataload \
  && apt-get update && apt-get install -y pgloader jq curl git zip unzip sqlite3 binutils libproj-dev postgis python3 python3-pip \
                                          build-essential libsqlite3-dev zlib1g-dev postgresql-client \
                                          sbcl make gawk freetds-dev libzip-dev \
  && rm -rf /var/lib/apt/lists/* \
  && curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
  && chmod +x mc && cp mc /usr/local/bin/mc \
  && mkdir -p /dataload/tmp/tippecanoe-src \
  && git clone https://github.com/mapbox/tippecanoe.git /dataload/tmp/tippecanoe-src \
  && cd /dataload/tmp/tippecanoe-src && make && make install && cd /dataload && rm -rf /dataload/tmp/tippecanoe-src \
  && pip3 install mapboxcli \
  && git clone https://github.com/dimitri/pgloader.git /dataload/tmp/pgloader \
  && cd /dataload/tmp/pgloader && make pgloader && cp ./build/bin/pgloader /usr/local/bin/pgloader && pgloader --help

USER 1021
CMD ["/dataload/load_hydat.sh"]
