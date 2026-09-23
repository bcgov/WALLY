import os
import subprocess
import sys
from datetime import datetime, date
import threading

DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
ENDPOINT_URL = os.environ["AWS_ENDPOINT_URL"]
S3_PATH = f"s3://{os.getenv('BUCKET_NAME')}/{date.today()}-{DB_NAME}.dump"
os.environ["PGPASSWORD"] = DB_PASSWORD

def log_stream(stream, prefix):
    """Stream stderr output with timestamps"""
    for line in stream:
        print(f"{datetime.now()} [{prefix}] {line.decode().strip()}")

pg_dump_cmd = [
    "pg_dump",
    "-h", DB_HOST,
    "-p", DB_PORT,
    "-U", DB_USER,
    "-d", DB_NAME,
    "-Fc",
    "-v"
]

aws_cp_cmd = [
    "aws", "s3", "cp", "-", S3_PATH,
    "--endpoint-url", ENDPOINT_URL,
    "--debug",
    "--expected-size", "60000000000"
]

print(f"Starting backup to {S3_PATH} at {datetime.now()}")



try:
    dump_proc = subprocess.Popen(pg_dump_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    aws_proc = subprocess.Popen(aws_cp_cmd, stdin=dump_proc.stdout, stderr=subprocess.PIPE)

    dump_proc.stdout.close()

    dump_thread = threading.Thread(target=log_stream, args=(dump_proc.stderr, "pg_dump"))
    aws_thread = threading.Thread(target=log_stream, args=(aws_proc.stderr, "aws"))

    dump_thread.start()
    aws_thread.start()

    dump_thread.join()
    aws_thread.join()

    if dump_proc.wait() != 0:
        print("pg_dump failed!")
        sys.exit(1)
    if aws_proc.wait() != 0:
        print("AWS upload failed!")
        sys.exit(1)

    print(f"Backup completed successfully at {datetime.now()}")
    print(f"Saved to: {S3_PATH}")

except Exception as e:
    print(f"Backup failed at {datetime.now()}: {str(e)}")
    sys.exit(1)
