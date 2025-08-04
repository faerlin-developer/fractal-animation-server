import logging
import signal
import sys

import httpx

from common.db.sql.tables.task import State
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


def generate_julia_animation(z_re, z_im, width=800, height=600, max_iterations=500, scale=1.2, filename="julia.mp4"):
	julia = JuliaAnimation(width=width, height=height, max_iterations=max_iterations, c=(z_re, z_im), scale=scale)
	julia.generate_and_save(filename)


def main():
	logger.info("Starting worker...")

	while not stop:

		# Get task from redis queue (returns None if timeout)
		task = task_queue.pop(timeout=5)
		if task is None:
			continue

		logger.info(f"Processing task: {task}")

		try:
			# generate_julia_set(task.z_re, task.z_im, filename="julia.png")
			generate_julia_animation(task.z_re, task.z_im, filename="julia.mp4")
			file_path = f"julia.mp4"
			object_name = f"{task.id}.mp4"
			# object_storage.put(bucket_name, object_name, file_path, "image/png")
			object_storage.put(bucket_name, object_name, file_path, "video/mp4")
			logger.info(f"Uploaded '{file_path}' as '{object_name}' in bucket '{bucket_name}'")
		except Exception as e:
			logger.info(f"Upload failed: {e}")
			payload = {"state": State.FAILED.value}
			with httpx.Client() as client:
				client.put(f"http://task-master-service:8000/update/{task.id}", json=payload)
			continue

		# Update state of task
		payload = {"state": State.DONE.value}
		with httpx.Client() as client:
			client.put(f"http://task-master-service:8000/update/{task.id}", json=payload)


if __name__ == "__main__":
	main()
