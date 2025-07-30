import json
import logging
import signal
import sys
import time

import redis
from minio import Minio, S3Error

from app.common.db.task import FractalTask
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
	logger.info("generated sample")


def generate_julia_set(z_re, z_im, width=800, height=600, max_iterations=500, scale=1.2, filename="julia.png"):
	"""Generate julia set"""

	julia = Julia(
		width=width,
		height=height,
		max_iterations=max_iterations,
		c=(z_re, z_im),
		scale=scale
	)

	julia.generate(filename)

	logger.info("generated sample")


def main():
	"""
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
	"""

	logger.info("Starting worker...")

	while not stop:
		try:
			entry = r.blpop([QUEUE_NAME], timeout=5)
			if entry:
				_, task_bytes = entry

				task_dict = json.loads(task_bytes)
				task = FractalTask(**task_dict)

				logger.info(f"Processing task: {task}")

				generate_julia_set(task.z_re, task.z_im, filename="julia.png")

				object_name = f"{task.id}.png"
				file_path = f"julia.png"

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

				# Move this to GET /download of task master
				url = client.presigned_get_object("images", f"{task.id}.png")

				logger.info(f'Access your image: {url}')

		except Exception as e:
			logger.error(e)
			time.sleep(1)


if __name__ == "__main__":
	main()
