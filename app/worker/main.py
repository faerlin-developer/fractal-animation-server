import logging
import signal
import sys
import time

import redis
from minio import Minio
from minio.error import S3Error

from julia import Julia

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

stop = False

bucket_name = "images"

r = redis.Redis(host='redis-service', port=6379)

# Connect to your MinIO server
client = Minio(
    "172.17.0.1:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)


def handle_signal(signum, frame):
    global stop
    logger.info("Received SIGTERM or SIGINT, cleaning up...")
    stop = True
    # Do your cleanup here
    stop = True


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

QUEUE_NAME = "task_queue"


def generate_sample():
    julia = Julia(
        width=800,
        height=600,
        max_iterations=500,
        c=(-0.80, -0.18),
        scale=1.2
    )

    julia.generate()
    logger.info("Generated sample")


def main():
    generate_sample()

    object_name = "julia.png"  # Object key in bucket
    file_path = "/app/worker/julia.png"  # Local path to fil

    try:
        # Upload the file
        client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path,
            content_type="image/png"
        )
        logger.info(f"Uploaded '{file_path}' as '{object_name}' in bucket '{bucket_name}'")
    except S3Error as e:
        logger.info(f"Upload failed: {e}")

    logger.info("Starting worker...")

    while True:
        try:
            # BLPOP returns (key, value) if something is available
            task = r.blpop([QUEUE_NAME], timeout=5)  # 5-second block
            if task:
                key, value = task
                logger.info(f"Processing task: {value}")

                url = client.presigned_get_object("images", "julia.png")
                # external_host = "localhost:30900"
                # parsed = urlparse(url)
                # public_url = urlunparse(parsed._replace(netloc=external_host))
                logger.info(f'Access your image: {url}')

        except Exception as e:
            logger.error(e)
            time.sleep(1)


if __name__ == "__main__":
    main()
