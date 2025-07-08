
build-images: task_master image_server

task_master:
	docker build \
		-f deploy/docker/dockerfile.task_master \
		-t $(TASK_MASTER_IMAGE) \
		--build-arg BUILD_REF=$(VERSION) \
		--build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
		.

image_server:
	docker build \
		-f deploy/docker/dockerfile.image_server \
		-t $(IMAGE_SERVER_IMAGE) \
		--build-arg BUILD_REF=$(VERSION) \
		--build-arg BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ") \
		.