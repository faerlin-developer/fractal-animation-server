curl:
	curl -X GET http://task-master-service:8000/tasks -H "Content-Type: application/json" -d '{"body":"This is a post"}'