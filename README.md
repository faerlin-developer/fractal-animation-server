# fractals-as-a-service

## Endpoints

### Task Master

|      |           | Request Payload                             | Response Payload | Description |
|------|-----------|---------------------------------------------|------------------|-------------|
| POST | `/add`    | task, JWT (include username)                |                  |             |
| POST | `/delete` | task, JWT (include username)                |                  |             |
| GET  | `/tasks`  | status of all tasks, JWT (include username) |                  |             |
|      |           |                                             |                  |             |

### Auth Server

|      |            | Request Payload   | Response Payload | Description |
|------|------------|-------------------|------------------|-------------|
| POST | `/sign-up` | username,password |                  |             |
| GET  | `/sign-in` | username          | JWT              |             |

### Image Server

|     |             | Request Payload | Response Payload | Description |
|-----|-------------|-----------------|------------------|-------------|
| GET | `/download` | task id         | image            |             |

## Traefik Setup

```bash
traefik-path-routing/
├── 01-traefik-rbac.yaml
├── 02-traefik-deployment.yaml
├── 03-traefik-service.yaml
├── 04-task-master-deployment.yaml
├── 05-task-master-service.yaml
├── 06-image-server-deployment.yaml
├── 07-image-server-service.yaml
├── 08-ingress-path-routing.yaml
```

## Notes

- RBAC grants access to pods
- An Ingress is a Kubernetes resource that define rules for routing external HTTP(s) traffic to services inside the
  cluster.
- An Ingres Controler is the actual gatekeeper — the thing that listens on port 80/443 and knows what to do based on the
  Ingress rules. Example: traefik. It reads Kubernetes Ingress resources. Then it dynamically configures itself to
  route traffic to the appropriate services.
- The traefik's NodePort exposes Traefik on a fixed port outside of the cluster.

## TODO

1. Replace httpie calls to pytest files
2. MinIO should be outside of the cluster.
    - Remove existing MinIO inside cluster
    - Database initializer should get host IP from ENV
    - Worker should get host IP from ENV
    - Use Kubernetes ConfigMap or Secrets to set ENV

  ```
  minio:
	docker run -p 9000:9000 -p 9001:9001 \
		-e MINIO_ROOT_USER=minioadmin \
  		-e MINIO_ROOT_PASSWORD=minioadmin123 \
  		quay.io/minio/minio server /data --console-address ":9001" --address ":9000"


  host-ip:
    # Host IP from perspective of containers
	ip -4 addr show docker0 | grep inet
  ```

  ```
  FROM python:3.11-slim

  # Define build-time args (will be passed from CLI)
  ARG MINIO_ENDPOINT
  ARG MINIO_ACCESS_KEY
  ARG MINIO_SECRET_KEY

  # Promote to runtime environment variables
  ENV MINIO_ENDPOINT=$MINIO_ENDPOINT
  ENV MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY
  ENV MINIO_SECRET_KEY=$MINIO_SECRET_KEY

  WORKDIR /app
  COPY . .

  CMD ["python", "main.py"]
  ```

  ```bash
  xargs < .env.build docker build -t my-image --build-arg
  ```

```python
import os

endpoint = os.getenv("MINIO_ENDPOINT")
access_key = os.getenv("MINIO_ACCESS_KEY")
secret_key = os.getenv("MINIO_SECRET_KEY")

print("Connecting to MinIO at:", endpoint)
```

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: minio-config
data:
  MINIO_ENDPOINT: "172.17.0.1:9000"
  MINIO_BUCKET: "images"
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: minio-secret
type: Opaque
stringData: # You can use plain text here; K8s encodes it automatically
  MINIO_ACCESS_KEY: minioadmin
  MINIO_SECRET_KEY: minioadmin123
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: worker
  template:
    metadata:
      labels:
        app: worker
    spec:
      containers:
        - name: worker
          image: your-docker-image:latest
          envFrom:
            - configMapRef:
                name: minio-config
            - secretRef:
                name: minio-secret
```