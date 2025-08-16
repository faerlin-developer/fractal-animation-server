from minio import Minio


class ObjectStorage:

	def __init__(self, host: str, port: int, access_key: str, secret_key: str):
		self.client = Minio(
			f"{host}:{port}",
			access_key=access_key,
			secret_key=secret_key,
			secure=False
		)

	def put(self, bucket_name, object_name, file_path, content_type):
		self.client.fput_object(
			bucket_name=bucket_name,
			object_name=object_name,
			file_path=file_path,
			content_type=content_type
		)

	def get(self, bucket_name: str, object_name: str):
		return self.client.presigned_get_object(bucket_name, object_name)
