httpie-task-master:
	http -v GET localhost:30080/tasks body="GET /tasks"
	http -v POST localhost:30080/add body="POST /add"
	http -v POST localhost:30080/delete body="POST /delete"

httpie-image-server:
	http -v GET localhost:30080/download body="GET /download"

httpie-user-manager:
	http -v POST localhost:30080/sign-up body="POST /sign-up"
	http -v GET localhost:30080/sign-in body="GET /sign-in"
