from dataclasses import dataclass


@dataclass
class Config:
	"""Class for configuration parameters"""

	# Secret (Loaded from Kubernetes secret volume)
	minio_username: str = ""
	minio_password: str = ""

	# Redis parameters
	redis_host: str = "redis-service"
	redis_port: int = 6379

	# Minio parameters
	minio_host: str = "172.17.0.1"
	minio_port: int = 9000
	minio_bucket_name = "images"

	# Task master parameters
	task_master_host = "task-master-service"
	task_master_port = 8000

	# Julia animation parameters
	default_width = 800
	default_height = 600
	default_max_iterations = 500
	default_scale = 1.2

	def load_secrets(self):
		self.minio_username = self.read_secret("/etc/secret/minio_username")
		self.minio_password = self.read_secret("/etc/secret/minio_password")

	@staticmethod
	def read_secret(path: str) -> str:
		with open(path, "r") as f:
			return f.read().strip()


cfg = Config()
cfg.load_secrets()
