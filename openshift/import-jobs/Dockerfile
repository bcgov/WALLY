FROM debian

WORKDIR /dataload
RUN useradd wally -M -G root -u 1021 && chmod -R 775 /dataload \
  && chown -R wally:root /dataload \
  && apt-get update && apt-get install -y pgloader curl zip unzip sqlite3 binutils libproj-dev gdal-bin \
  && rm -rf /var/lib/apt/lists/* \
  && curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
  && chmod +x mc

COPY ./hydat/load_hydat.sh /dataload
COPY ./databc/load_layer_data.sh /dataload
COPY ./databc/download_layer.sh /dataload
USER 1021
CMD ["/dataload/load_hydat.sh"]
