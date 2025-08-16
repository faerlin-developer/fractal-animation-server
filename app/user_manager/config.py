from dataclasses import dataclass


@dataclass
class Config:
	"""Class for configuration parameters"""

	# Secret (Loaded from Kubernetes secret volume)
	database_url: str = ""

	def load_secrets(self):
		self.database_url = self.read_secret("/etc/secret/database_url")

	@staticmethod
	def read_secret(path: str) -> str:
		with open(path, "r") as f:
			return f.read().strip()


cfg = Config()
cfg.load_secrets()
