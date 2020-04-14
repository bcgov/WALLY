FROM debian

WORKDIR /dataload
RUN useradd wally -M -G root -u 1021 && chmod -R 775 /dataload \
  && chown -R wally:root /dataload \
  && apt-get update && apt-get install -y pgloader jq curl git zip unzip sqlite3 binutils libproj-dev gdal-bin postgis python3 python3-pip \
                                          build-essential libsqlite3-dev zlib1g-dev postgresql-client \
  && rm -rf /var/lib/apt/lists/* \
  && curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
  && chmod +x mc && cp mc /usr/local/bin/mc \
  && mkdir -p /dataload/tmp/tippecanoe-src \
  && git clone https://github.com/mapbox/tippecanoe.git /dataload/tmp/tippecanoe-src \
  && cd /dataload/tmp/tippecanoe-src && make && make install && cd /dataload && rm -rf /dataload/tmp/tippecanoe-src \
  && pip3 install mapboxcli

COPY ./hydat/load_hydat.sh /dataload/
COPY ./databc/*.sh /dataload/
COPY ./prism/*.sh /dataload/
COPY ./tiles/create_tileset.sh /dataload/
COPY ./tiles/upload_tileset.sh /dataload/


USER 1021
CMD ["/dataload/load_hydat.sh"]
