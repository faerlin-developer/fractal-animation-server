import logging
import signal
import sys
import time

from minio import S3Error

from worker.db.clients import object_storage
from worker.db.clients import task_queue
from worker.julia.animation import JuliaAnimation
from worker.julia.image import JuliaImage

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

stop = False

bucket_name = "images"


def handle_signal(signum, frame):
	global stop
	logger.info("Received SIGTERM or SIGINT, cleaning up...")
	stop = True


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

QUEUE_NAME = "task_queue"


def generate_julia_set(z_re, z_im, width=800, height=600, max_iterations=500, scale=1.2, filename="julia.png"):
	"""Generate julia set"""

	julia = JuliaImage(
		width=width,
		height=height,
		max_iterations=max_iterations,
		c=(z_re, z_im),
		scale=scale
	)

	julia.generate()
	julia.save(filename)

	logger.info(f"generated {filename}")


def main():
	logger.info("Starting worker...")

	while not stop:
		try:

			# Get task from redis queue (returns None if timeout)
			task = task_queue.pop(timeout=5)
			if task is None:
				continue

			logger.info(f"Processing task: {task}")

			generate_julia_set(task.z_re, task.z_im, filename="julia.png")

			object_name = f"{task.id}.png"
			file_path = f"julia.png"

			try:
				object_storage.put(bucket_name, object_name, file_path, "image/png")
				logger.info(f"Uploaded '{file_path}' as '{object_name}' in bucket '{bucket_name}'")
			except S3Error as e:
				logger.info(f"Upload failed: {e}")

			url = object_storage.get(bucket_name, object_name)
			logger.info(f'Access your image: {url}')

		except Exception as e:
			logger.error(e)
			time.sleep(1)


if __name__ == "__main__":
	julia = JuliaAnimation(width=800, height=600, max_iterations=500, c=(-0.80, -0.18), scale=1.2)
	julia.generate()

	main()
