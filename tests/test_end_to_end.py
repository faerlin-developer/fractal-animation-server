import time

import httpx

from app.common.db.sql.tables.task import State
from app.common.security.token import verify_jwt

HOST_PORT = "http://localhost:30080"


def signup_user(username: str, password: str):
	"""Send POST /sign-up request"""

	payload = {
		"username": username,
		"password": password,
	}

	response = None
	with httpx.Client() as client:
		response = client.post(f"{HOST_PORT}/sign-up", json=payload)

	return response


def signin_user(username: str, password: str):
	"""Send POST /sign-in request"""

	payload = {
		"username": username,
		"password": password,
	}

	response = None
	with httpx.Client() as client:
		response = client.post(f"{HOST_PORT}/sign-in", json=payload)

	return response


def delete_user(token: str):
	"""Send DELETE /delete-user request"""

	headers = {
		"Authorization": f"Bearer {token}"
	}

	response = None
	with httpx.Client() as client:
		response = client.delete(f"{HOST_PORT}/delete-user", headers=headers)

	return response


def add_task(task: dict, token: str):
	"""Send POST /add request"""

	headers = {
		"Authorization": f"Bearer {token}"
	}

	response = None
	with httpx.Client() as client:
		response = client.post(f"{HOST_PORT}/add", json=task, headers=headers)

	return response


def get_task(task_id: str, token: str):
	"""Send POST /download/{task_id} request"""

	headers = {
		"Authorization": f"Bearer {token}"
	}

	response = None
	with httpx.Client() as client:
		response = client.get(f"{HOST_PORT}/task/{task_id}", headers=headers)

	return response


def test_end_to_end():
	"""End-to-end test"""

	username = "faerlin"
	password = "<PASSWORD>"

	# POST /sign-up
	response = signup_user(username, password)
	assert response.status_code == 201

	data = response.json()
	assert "id" in data and "username" in data
	assert data["username"] == username

	# POST /sign-in
	response = signin_user(username, password)
	assert response.status_code == 201

	data = response.json()
	token = data["access_token"]
	claims = verify_jwt(token=token)
	assert "sub" in claims and "exp" in claims
	assert claims["sub"] == username

	# POST /add
	task = {"z_re": -0.80, "z_im": -0.18}
	response = add_task(task, token)
	assert response.status_code == 201

	data = response.json()
	assert "id" in data
	assert task.items() <= data.items()
	task_id = data["id"]

	# GET /task/{task_id}
	# Poll until task is done
	i = 0
	while True:
		response = get_task(task_id, token)
		data = response.json()
		assert data["id"] == task_id

		if data["state"] == State.DONE.value:
			print(data)
			break
		elif data["state"] == State.FAILED.value:
			print("task failed")
			break
		else:
			print(f"i={i} sleeping 2 second")
			i += 1
			time.sleep(2)

	# DELETE /delete-user
	response = delete_user(token)
	assert response.status_code == 204
