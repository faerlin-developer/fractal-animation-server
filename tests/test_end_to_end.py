import httpx

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


def test_end_to_end():
    """End-to-end test"""

    username = "faerlin"
    password = "<PASSWORD>"

    # POST /sign-up
    response = signup_user(username, password)
    assert response.status_code == 201

    data = response.json()
    assert "id" in data
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

    # DELETE /delete-user
    response = delete_user(token)
    assert response.status_code == 204
