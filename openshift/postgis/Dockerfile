
FROM registry.access.redhat.com/rhscl/postgresql-10-rhel7:latest

# The base image exposes port 5432, we just need to take it and
# and apply our changes on top of it.

USER 0

ENV PATH=$HOME/.local/bin/:$PATH \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
   
ENV SUMMARY="PostgreSQL 10 with PostGIS 2.5 extension." \
    DESCRIPTION="This image extends the RHEL7 base PostgreSQL 10 \
image by adding PostGIS 2.5 from postgresql.org and dependencies \
from fedoraproject.org needed to support GDAL."

LABEL summary="$SUMMARY" \
  description="$DESCRIPTION" \
  io.k8s.description="$DESCRIPTION" \
  io.k8s.display-name="PostgreSQL 10 with PostGIS 2.5" \
  io.openshift.expose-services="5432:http" \
  io.openshift.tags="postgres,postgis" \
  release="1"

RUN yum repolist > /dev/null && \
    yum install -y yum-utils && \
    yum-config-manager --disable \* &> /dev/null && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum-config-manager --enable rhel-7-server-rpms && \
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum-config-manager --enable rhel-7-server-extras-rpms && \
    yum-config-manager --enable rhel-7-server-fastrack-rpms && \
    yum install curl && \
    curl -O https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-redhat10-10-2.noarch.rpm && \
    curl -O https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum -y localinstall pgdg-redhat10-10-2.noarch.rpm epel-release-latest-7.noarch.rpm && \
    yum -y update && \
    rm -f pgdg-redhat10-10-2.noarch.rpm && \
    rm -f epel-release-latest-7.noarch.rpm

# The RHEL Extra Packages for Enterprise Linux (EPEL) package `epel-release` 
# is required gdal-libs dependencies. 

RUN yum list epel\* && \
    yum list post\* && \
    yum -y install epel-release postgis25_10.x86_64 postgis25_10-client.x86_64 postgis25_10-utils.x86_64 && \
    yum clean all -y

# The install does not put them in the same place as the other PostgreSQL extensions
# so let's move them.

RUN diff --brief -r \
    /opt/rh/rh-postgresql10/root/usr/share/pgsql/extension /usr/pgsql-10/share/extension | \
    grep '/usr/pgsql-10/share/extension' | \
    tr ':' '/' |  \
    awk '{ print $3 $4 }' | \
    xargs cp -vt /opt/rh/rh-postgresql10/root/usr/share/pgsql/extension && \
    cp -a /usr/pgsql-10/share/contrib/* /opt/rh/rh-postgresql10/root/usr/share/pgsql/contrib/ && \
    diff --brief /usr/pgsql-10/lib /opt/rh/rh-postgresql10/root/usr/lib64/pgsql | \
    grep -v '/opt/rh/rh-postgresql10/root/usr/lib64/pgsql' | \
    tr ':' '/' |  \
    awk '{ print $3 $4 }' | \
    xargs cp -vt /opt/rh/rh-postgresql10/root/usr/lib64/pgsql && \
    cp -a /usr/pgsql-10/bin/pgsql2shp /usr/pgsql-10/bin/raster2pgsql \
    /usr/pgsql-10/bin/shp2pgsql /opt/rh/rh-postgresql10/root/usr/bin/ && \
    rm -rf /usr/pgsql-10

# PostgreSQL user in /etc/passwd
USER 26
