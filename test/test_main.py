"""
Tests
"""
import pytest
from flask.testing import FlaskClient

from src import main


def test_validate_users_password(authorized_auth: dict, unauthorized_auth: dict) -> None:
    """
    Unit test
    """
    assert main.validate_username_password(
        authorized_auth["username"], authorized_auth["password"]
    )
    assert not main.validate_username_password(
        unauthorized_auth["username"], unauthorized_auth["password"]
    )


def test_get_box_platform_access_token() -> None:
    """
    Integration test that calls Box Platform
    """
    assert main.get_box_platform_access_token()


def test_authorized_token_request(client: FlaskClient, token_endpoint: str, authorized_header: dict) -> None:
    """
    Functional test for valid credentials
    """
    resp = client.get(token_endpoint, headers=authorized_header)
    response_data = resp.get_json()
    access_token = response_data.get("access_token")
    assert resp.status_code == 200
    assert access_token


def test_unauthorized_token_request(client: FlaskClient, token_endpoint: str, unauthorized_header: dict) -> None:
    """
    Functional test for invalid credentials
    """
    resp = client.get(token_endpoint, headers=unauthorized_header)
    response_data = resp.get_json()
    assert resp.status_code == 401
    assert response_data.get("message") == "Unauthorized"
