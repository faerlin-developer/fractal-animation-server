
KIND_IMAGE         := kindest/node:v1.30.13
KIND_CLUSTER       := faas-cluster
TASK_MASTER_APP    := task-master
IMAGE_SERVER_APP   := image-server
VERSION            := 0.0.1
BASE_IMAGE_NAME    := faas
TASK_MASTER_IMAGE  := $(BASE_IMAGE_NAME)/$(TASK_MASTER_APP):$(VERSION)
IMAGE_SERVER_IMAGE  := $(BASE_IMAGE_NAME)/$(IMAGE_SERVER_APP):$(VERSION)
