from minio import Minio
from api.config import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST_URL


# minio_client = Minio(MINIO_HOST_URL,
#                   access_key=MINIO_ACCESS_KEY,
#                   secret_key=MINIO_SECRET_KEY,
#                   secure=False)

minio_client = Minio("minio-bfpeyx-dev.pathfinder.gov.bc.ca",
                  access_key="BK5o5xdo",
                  secret_key="quIAVbQiX3euO8jH",
                  secure=True)