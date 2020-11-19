from minio import Minio
from api.config import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_HOST_URL


minio_client = Minio(MINIO_HOST_URL,
                  access_key=MINIO_ACCESS_KEY,
                  secret_key=MINIO_SECRET_KEY,
                  secure=False)
