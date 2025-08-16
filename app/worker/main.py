import signal

import structlog

import common.logger.slog  # noqa: F401
from common.db.sql.tables.task import State
from worker.config import cfg
from worker.db.clients import object_storage
from worker.db.clients import task_queue
from worker.http.clients import task_master_client
from worker.julia.animation import JuliaAnimation

log = structlog.get_logger()
stop = False


def handle_signal(signum, frame):
	global stop
	log.info("handle signal", signum=signum, frame=frame)
	stop = True


signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)


def generate_julia_animation(z_re, z_im, filename, width, height, max_iterations, scale):
	julia = JuliaAnimation(width=width, height=height, max_iterations=max_iterations, c=(z_re, z_im), scale=scale)
	julia.generate_and_save(filename)
	log.info("generated julia set animation", filename=filename)


def main():
	log.info("started worker")

	while not stop:

		# Get task from redis queue (returns None if timeout)
		task = task_queue.pop(timeout=1)
		if task is None:
			continue

		log.info("Started to process task", task=task)

		try:
			# Generate Julia animation locally
			local_file = f"julia.mp4"
			generate_julia_animation(z_re=task.z_re,
									 z_im=task.z_im,
									 filename=local_file,
									 width=cfg.default_width,
									 height=cfg.default_height,
									 max_iterations=cfg.default_max_iterations,
									 scale=cfg.default_scale)

			# Store object in storage
			object_name = f"{task.id}.mp4"
			object_storage.put(cfg.minio_bucket_name, object_name, local_file, "video/mp4")
			log.info("upload file to object storage", object_name=object_name, bucket_name=cfg.minio_bucket_name)

			# Update state of task to DONE
			task_master_client.update_state(task.id, State.DONE.value)

		except Exception as exception:
			log.error("failed to upload file to object storage", exception=exception, task=task)
			task_master_client.update_state(task.id, State.FAILED.value)


if __name__ == "__main__":
	main()
