import logging
import sys

from minio import Minio
from minio.error import S3Error
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

bucket_name = "images"

DATABASE_URL = "postgresql://myuser:mypassword@postgres-service:5432/mydb"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
)

metadata.create_all(engine)

logging.info("Tables created.")

# Connect to your MinIO server
client = Minio(
    "172.17.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin123",
    secure=False
)

# Create the bucket if it doesn't exist
try:
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logging.info(f"Bucket {bucket_name} created.")
    else:
        logging.info(f"Bucket {bucket_name} already exists.")
except S3Error as e:
    logging.info(f"Failed to create bucket: {e}")
