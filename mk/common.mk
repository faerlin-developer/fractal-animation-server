
# Cluster
KIND_IMAGE          := kindest/node:v1.30.13
KIND_CLUSTER        := faas-cluster

# Applications
VERSION             := 0.0.1
BASE_IMAGE_NAME     := faas
TASK_MASTER_APP     := task-master
USER_MANAGER_APP    := user-manager
WORKER_APP 		    := worker
POSTGRES_APP        := postgres
FRONTEND_APP		:= frontend
TASK_MASTER_IMAGE   := $(BASE_IMAGE_NAME)/$(TASK_MASTER_APP):$(VERSION)
USER_MANAGER_IMAGE  := $(BASE_IMAGE_NAME)/$(USER_MANAGER_APP):$(VERSION)
WORKER_IMAGE        := $(BASE_IMAGE_NAME)/$(WORKER_APP):$(VERSION)
POSTGRES_IMAGE      := $(BASE_IMAGE_NAME)/$(POSTGRES_APP):$(VERSION)
FRONTEND_IMAGE      := $(BASE_IMAGE_NAME)/$(FRONTEND_APP):$(VERSION)
