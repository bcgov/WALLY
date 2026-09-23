#!/usr/bin/env python3
"""
dump_minio.py

Copies every object from every known Wally Minio bucket into an S3
intermediary bucket, under a timestamped prefix.

Reads: prod Minio (expects read-only credentials - this script never calls
       delete_object/delete_objects/put_object against the source, only
       list_objects_v2 and get_object).
Writes: S3 intermediary bucket only.

Required env vars:
  MINIO_HOST_URL       e.g. http://wally-prod-minio:9000
  MINIO_ACCESS_KEY     prod, read-only
  MINIO_SECRET_KEY     prod, read-only

  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  S3_BUCKET            intermediary bucket name
  S3_PREFIX            optional - defaults to a fresh UTC timestamp,
                        e.g. wally-minio-2026-08-14T22-10-00Z
"""

import os
import sys
import datetime
import boto3
from botocore.exceptions import ClientError

BUCKETS_TO_BACKUP = ['files', 'geojson', 'mbtiles', 'other', 'projects', 'raster']


def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=os.environ['MINIO_HOST_URL'],
        aws_access_key_id=os.environ['MINIO_ACCESS_KEY'],
        aws_secret_access_key=os.environ['MINIO_SECRET_KEY'],
        region_name='us-east-1',
    )


def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
    )


def default_prefix():
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
    return f'wally-minio-{ts}'


def dump_bucket(minio_client, s3_client, bucket, s3_bucket, s3_prefix):
    object_count = 0
    total_bytes = 0

    try:
        paginator = minio_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket):
            for obj in page.get('Contents', []):
                key = obj['Key']
                size = obj.get('Size', 0)
                dest_key = f'{s3_prefix}/{bucket}/{key}'

                print(f'  {bucket}/{key} ({size} bytes) -> s3://{s3_bucket}/{dest_key}')

                body = minio_client.get_object(Bucket=bucket, Key=key)['Body'].read()
                s3_client.put_object(Bucket=s3_bucket, Key=dest_key, Body=body)

                object_count += 1
                total_bytes += size
    except ClientError as exc:
        code = exc.response.get('Error', {}).get('Code', '')
        if code in ('NoSuchBucket', '404'):
            print(f'  WARNING: bucket {bucket!r} does not exist on source - skipping.')
            return 0, 0
        raise

    return object_count, total_bytes


def main():
    s3_bucket = os.environ['S3_BUCKET']
    s3_prefix = os.environ.get('S3_PREFIX') or default_prefix()

    minio_client = get_minio_client()
    s3_client = get_s3_client()

    print(f'Dumping Minio -> s3://{s3_bucket}/{s3_prefix}/')
    print(f'Buckets: {", ".join(BUCKETS_TO_BACKUP)}')
    print()

    grand_total_objects = 0
    grand_total_bytes = 0
    summary = []

    for bucket in BUCKETS_TO_BACKUP:
        print(f'Bucket: {bucket}')
        count, size = dump_bucket(minio_client, s3_client, bucket, s3_bucket, s3_prefix)
        summary.append((bucket, count, size))
        grand_total_objects += count
        grand_total_bytes += size
        print()

    print('=' * 60)
    print('Summary')
    print('=' * 60)
    for bucket, count, size in summary:
        print(f'  {bucket:12s}  {count:6d} objects  {size:>14,d} bytes')
    print('-' * 60)
    print(f'  {"TOTAL":12s}  {grand_total_objects:6d} objects  {grand_total_bytes:>14,d} bytes')
    print()
    print(f'Backup location: s3://{s3_bucket}/{s3_prefix}/')
    print('Finished.')

    if grand_total_objects == 0:
        print('WARNING: zero objects were copied. Check source bucket names '
              'and credentials - this may indicate a silent misconfiguration '
              'rather than a genuinely empty Minio instance.', file=sys.stderr)


if __name__ == '__main__':
    main()