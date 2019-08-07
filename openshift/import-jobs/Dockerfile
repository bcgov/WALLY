FROM debian
RUN apt-get update && apt-get install -y pgloader \
    && rm -rf /var/lib/apt/lists/* 
WORKDIR /dataload
COPY ./hydat/load_hydat.sh /dataload
CMD ["/dataload/load_hydat.sh"]
