
kind-create:
	kind create cluster \
		--image $(KIND_IMAGE) \
		--name $(KIND_CLUSTER) \
		--config deploy/kind/config.yaml

kind-delete:
	kind delete cluster --name $(KIND_CLUSTER)

kind-load:
	kind load docker-image $(TASK_MASTER_IMAGE) --name $(KIND_CLUSTER)
	kind load docker-image $(USER_MANAGER_IMAGE) --name $(KIND_CLUSTER)
	kind load docker-image $(WORKER_IMAGE) --name $(KIND_CLUSTER)
	kind load docker-image $(POSTGRES_IMAGE) --name $(KIND_CLUSTER)
