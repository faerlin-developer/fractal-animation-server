
docker-build: task_master user_manager

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