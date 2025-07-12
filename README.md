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