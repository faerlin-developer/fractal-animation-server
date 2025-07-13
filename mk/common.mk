
KIND_IMAGE         := kindest/node:v1.30.13
KIND_CLUSTER       := faas-cluster
TASK_MASTER_APP    := task-master
USER_MANAGER_APP   := user-manager
VERSION            := 0.0.1
BASE_IMAGE_NAME    := faas
TASK_MASTER_IMAGE  := $(BASE_IMAGE_NAME)/$(TASK_MASTER_APP):$(VERSION)
USER_MANAGER_IMAGE  := $(BASE_IMAGE_NAME)/$(USER_MANAGER_APP):$(VERSION)
