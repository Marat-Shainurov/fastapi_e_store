from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.models import User


def verify_email_for_tests(client: TestClient, username: str, verification_code: str) -> None:
    client.post(f"/users/{username}/verify-email?code={verification_code}")


def get_auth_header_for_tests(client: TestClient, username: str, password: str) -> dict[str, str]:
    auth_data = {
        "username": username,
        "password": password
    }
    response_token = client.post("/users/token", data=auth_data)
    assert response_token.json()["token_type"] == "bearer"

    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {response_token.json()['access_token']}"
    }
    return header


def delete_user_for_tests(user: User, db_session: Session) -> None:
    db_session.delete(user)
    db_session.commit()

