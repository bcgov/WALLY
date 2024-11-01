#!/bin/sh
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

mkdir -p $MINIO_DATA_DIR/files
mkdir -p $MINIO_DATA_DIR/projects
mkdir -p $MINIO_DATA_DIR/raster
mkdir -p $MINIO_DATA_DIR/other
mkdir -p $MINIO_DATA_DIR/geojson
mkdir -p $MINIO_DATA_DIR/mbtiles

/usr/bin/docker-entrypoint.sh $@
