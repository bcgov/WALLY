# ---- Stage 1: builder with full dnf, resolves plr_16 + R-devel + all deps ----
# Using rockylinux:9 instead of ubi9/ubi - UBI ships a curated/reduced package
# subset (no subscription = missing AppStream packages like flexiblas-devel,
# libtirpc-devel). Rocky is a full RHEL rebuild with the complete repo set,
# no entitlement/subscription needed.
FROM rockylinux:9 AS builder

RUN dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
    /usr/bin/crb enable && \
    dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm

RUN dnf install -y \
      --installroot=/build-root \
      --releasever=9 \
      --setopt=install_weak_deps=False \
      --nogpgcheck \
      plr_16 R-devel && \
    dnf clean all --installroot=/build-root

# ---- Stage 2: actual Crunchy image, no dnf/microdnf resolver needed here ----
FROM artifacts.developer.gov.bc.ca/bcgov-docker-local/crunchy-postgres-gis:ubi9-16.11-3.4-2550

USER root

COPY --from=builder /build-root/usr /usr
COPY --from=builder /build-root/etc/ld.so.conf.d /etc/ld.so.conf.d
RUN ldconfig

RUN Rscript -e 'install.packages("remotes", repos="https://cloud.r-project.org")'

RUN Rscript -e 'remotes::install_version("Rcpp", version = "1.0.6", repos = "https://cloud.r-project.org")' && \
    Rscript -e 'remotes::install_version("fasstr", version = "0.3.2", repos = "https://cloud.r-project.org")'

USER postgres