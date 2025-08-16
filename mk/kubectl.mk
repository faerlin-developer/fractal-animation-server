
kubectl-run-psql-client:
	kubectl run -i --tty psql-client --rm \
		--image=postgres:14.8 \
  		--env="PGPASSWORD=mypassword" \
  		--restart=Never -- \
  		psql -h postgres-service -U myuser -d mydb

kubectl-apply:

	# Secret
	kubectl apply -f deploy/kind/secret/secret.yaml

	# Postgres
	kubectl apply -f deploy/kind/postgres/persistent-volume.yaml
	kubectl apply -f deploy/kind/postgres/persistent-volume-claim.yaml
	kubectl apply -f deploy/kind/postgres/deployment.yaml
	kubectl apply -f deploy/kind/postgres/service.yaml

	kubectl wait --for=condition=ready pod -l app=postgres --timeout=60s

	# Redis
	kubectl apply -f deploy/kind/redis/deployment.yaml
	kubectl apply -f deploy/kind/redis/service.yaml

	kubectl wait --for=condition=ready pod -l app=redis --timeout=60s

	# Task Master
	kubectl apply -f deploy/kind/task-master/deployment.yaml
	kubectl apply -f deploy/kind/task-master/service.yaml

	# User Manager
	kubectl apply -f deploy/kind/user-manager/deployment.yaml
	kubectl apply -f deploy/kind/user-manager/service.yaml

	# Worker
	kubectl apply -f deploy/kind/worker/deployment.yaml
	kubectl apply -f deploy/kind/worker/service.yaml

	# Traefik
	kubectl apply -f deploy/kind/traefik/rbac.yaml
	kubectl apply -f deploy/kind/traefik/deployment.yaml
	kubectl apply -f deploy/kind/traefik/service.yaml
	kubectl apply -f deploy/kind/traefik/ingress.yaml

kubectl-secret:
	kubectl get secret secret-credentials -o yaml

kubectl-rollout:
	kubectl get deployments -o name | xargs -n1 kubectl rollout restart

kubectl-run-busybox:
	kubectl run busybox --image=busybox:1.35 --restart=Never -it -- sh
