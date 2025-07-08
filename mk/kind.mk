
kind-create:
	kind create cluster \
		--image $(KIND_IMAGE) \
		--name $(KIND_CLUSTER) \
		--config deploy/kind/kind-config.yaml

kind-load:
	kind load docker-image $(TASK_MASTER_IMAGE) --name $(KIND_CLUSTER)
	kind load docker-image $(IMAGE_SERVER_IMAGE) --name $(KIND_CLUSTER)

kind-apply:
	kubectl apply -f deploy/kind/task-master.yaml

kind-delete:
	kind delete cluster --name $(KIND_CLUSTER)


