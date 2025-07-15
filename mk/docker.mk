
docker-build: task_master user_manager worker postgres

task_master:
	docker build \
		-f deploy/docker/dockerfile.task_master \
		-t $(TASK_MASTER_IMAGE) \
		--build-arg BUILD_REF=$(VERSION) \
		--build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
		.

user_manager:
	docker build \
		-f deploy/docker/dockerfile.user_manager \
		-t $(USER_MANAGER_IMAGE) \
		--build-arg BUILD_REF=$(VERSION) \
		--build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
		.

worker:
	docker build \
		-f deploy/docker/dockerfile.worker \
		-t $(WORKER_IMAGE) \
		--build-arg BUILD_REF=$(VERSION) \
		--build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
		.

postgres:
	docker build \
		-f deploy/docker/dockerfile.postgres \
		-t $(POSTGRES_IMAGE) \
		--build-arg BUILD_REF=$(VERSION) \
		--build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
		.

docker-run-minio:
	docker run -d \
  		--name my_minio \
  		-e MINIO_ROOT_USER=minioadmin \
  		-e MINIO_ROOT_PASSWORD=minioadmin \
  		-p 9000:9000 \
  		-p 9001:9001 \
  		-v "$(PWD)/data":/data \
  		minio/minio server /data --console-address ":9001"
	docker run --rm \
  		--network container:my_minio \
  		-e MC_HOST_local="http://minioadmin:minioadmin@localhost:9000" \
  		minio/mc mb local/images
