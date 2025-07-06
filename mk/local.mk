deploy-task-master:
	uvicorn services.task_master.main:app --host 0.0.0.0 --port 8000 --reload

deploy-image-server:
	uvicorn services.image_server.main:app --host 0.0.0.0 --port 8001 --reload

httpie-task-master:
	http -v POST localhost:8000/tasks body="This is a post"

httpie-image-server:
	http -v POST localhost:8001 body="This is a post"
