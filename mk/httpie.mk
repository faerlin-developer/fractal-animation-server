httpie-task-master:
	http -v POST localhost:30080/add body="POST /add"
	http -v POST localhost:30080/delete body="POST /delete"
	http -v GET localhost:30080/tasks body="GET /tasks"
	http -v GET localhost:30080/download body="POST /download"

httpie-user-manager:
	http -v POST localhost:30080/sign-up username="Faerlin" password="<PASSWORD>"
	http -v GET localhost:30080/sign-in body="GET /sign-in"
