FROM debian

WORKDIR /dataload

RUN apt-get update && apt-get install -y pgloader curl unzip sqlite3 \
    && rm -rf /var/lib/apt/lists/* \
    && curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
    && chmod +x mc

COPY ./hydat/load_hydat.sh /dataload
COPY ./databc/load_layer_data.sh /dataload
CMD ["/dataload/load_hydat.sh"]
