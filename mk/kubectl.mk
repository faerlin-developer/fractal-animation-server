curl:
	curl -X GET http://task-master-service:8000/tasks -H "Content-Type: application/json" -d '{"body":"This is a post"}'

kubectl-run-psql-client:
	kubectl run -i --tty psql-client --rm \
		--image=postgres:14.8 \
  		--env="PGPASSWORD=mypassword" \
  		--restart=Never -- \
  		psql -h postgres-service -U myuser -d mydb