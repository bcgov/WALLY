#!/usr/bin/env python3
"""
restore_minio.py

Copies every object under a given S3 intermediary prefix into staging's
Minio buckets.

Reads: S3 intermediary bucket only.
Writes: staging Minio (expects buckets to already exist, per the Minio
        entrypoint's `mkdir -p` step - this script never creates buckets,
        and never calls delete_object/delete_objects).

Required env vars:
  MINIO_HOST_URL       e.g. http://wally-staging-minio:9000
  MINIO_ACCESS_KEY     staging, write access
  MINIO_SECRET_KEY     staging, write access

  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  S3_BUCKET            intermediary bucket name
  S3_PREFIX            required - must match the prefix a prior dump_minio.py
                        run wrote to, e.g. wally-minio-2026-08-14T22-10-00Z
"""

import os
import sys
import boto3

BUCKETS_TO_RESTORE = ['files', 'geojson', 'mbtiles', 'other', 'projects', 'raster']


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


def restore_bucket(s3_client, minio_client, s3_bucket, s3_prefix, bucket):
    object_count = 0
    total_bytes = 0
    prefix = f'{s3_prefix}/{bucket}/'

    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=s3_bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            s3_key = obj['Key']
            size = obj.get('Size', 0)
            dest_key = s3_key[len(prefix):]

            if not dest_key:
                continue

            print(f'  s3://{s3_bucket}/{s3_key} -> {bucket}/{dest_key} ({size} bytes)')

            body = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)['Body'].read()
            minio_client.put_object(Bucket=bucket, Key=dest_key, Body=body)

            object_count += 1
            total_bytes += size

    return object_count, total_bytes


def main():
    s3_bucket = os.environ['S3_BUCKET']
    s3_prefix = os.environ.get('S3_PREFIX')

    if not s3_prefix:
        print('ERROR: S3_PREFIX is required for restore - refusing to guess '
              'which backup to restore from.', file=sys.stderr)
        sys.exit(1)

    minio_client = get_minio_client()
    s3_client = get_s3_client()

    print(f'Restoring s3://{s3_bucket}/{s3_prefix}/ -> Minio')
    print(f'Buckets: {", ".join(BUCKETS_TO_RESTORE)}')
    print()

    grand_total_objects = 0
    grand_total_bytes = 0
    summary = []

    for bucket in BUCKETS_TO_RESTORE:
        print(f'Bucket: {bucket}')
        count, size = restore_bucket(s3_client, minio_client, s3_bucket, s3_prefix, bucket)
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
    print('Finished.')

    if grand_total_objects == 0:
        print('WARNING: zero objects were restored. Check S3_PREFIX matches '
              'a real prior dump, and check credentials/bucket names.',
              file=sys.stderr)


if __name__ == '__main__':
    main()