
kind-create:
	kind create cluster \
		--image $(KIND_IMAGE) \
		--name $(KIND_CLUSTER) \
		--config deploy/kind/kind-config.yaml

kind-load:
	kind load docker-image $(TASK_MASTER_IMAGE) --name $(KIND_CLUSTER)
	kind load docker-image $(IMAGE_SERVER_IMAGE) --name $(KIND_CLUSTER)
	kind load docker-image $(USER_MANAGER_IMAGE) --name $(KIND_CLUSTER)

kind-apply:

	# Task Master
	kubectl apply -f deploy/kind/task-master/deployment.yaml
	kubectl apply -f deploy/kind/task-master/service.yaml

	# Image Server
	kubectl apply -f deploy/kind/image-server/deployment.yaml
	kubectl apply -f deploy/kind/image-server/service.yaml

	# User Manager
	kubectl apply -f deploy/kind/user-manager/deployment.yaml
	kubectl apply -f deploy/kind/user-manager/service.yaml

	# Traefik
	kubectl apply -f deploy/kind/traefik/rbac.yaml
	kubectl apply -f deploy/kind/traefik/deployment.yaml
	kubectl apply -f deploy/kind/traefik/service.yaml
	kubectl apply -f deploy/kind/traefik/ingress.yaml

kind-rollout:
	kubectl get deployments -o name | xargs -n1 kubectl rollout restart

kind-delete:
	kind delete cluster --name $(KIND_CLUSTER)

kind-run:
	kubectl run busybox --image=busybox:1.35 --restart=Never -it -- sh