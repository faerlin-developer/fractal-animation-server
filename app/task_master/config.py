from dataclasses import dataclass


@dataclass
class Config:
	"""Class for configuration parameters"""

	# Secret (Loaded from Kubernetes secret volume)
	database_url: str = ""
	minio_username: str = ""
	minio_password: str = ""

	# Non-secret
	redis_host: str = "redis-service"
	redis_port: int = 6379
	minio_host: str = "172.17.0.1"
	minio_port: int = 9000

	def load_secrets(self):
		self.database_url = self.read_secret("/etc/secret/database_url")
		self.minio_username = self.read_secret("/etc/secret/minio_username")
		self.minio_password = self.read_secret("/etc/secret/minio_password")

	@staticmethod
	def read_secret(path: str) -> str:
		with open(path, "r") as f:
			return f.read().strip()


cfg = Config()
cfg.load_secrets()
