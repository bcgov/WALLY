FROM rust:latest AS builder


RUN apt-get update && apt-get install -y musl-tools git && \
  rustup target add x86_64-unknown-linux-musl && \
  git clone https://github.com/mholling/whitebox-tools.git /wbt && \
  cd /wbt && git checkout d8_flow_accum-fix

WORKDIR /wbt

RUN cargo build --release --target x86_64-unknown-linux-musl
