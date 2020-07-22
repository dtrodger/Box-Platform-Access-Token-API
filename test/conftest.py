"""
Test fixtures
"""
import pytest
from _pytest.fixtures import FixtureFunctionMarker
from requests.auth import _basic_auth_str
from flask.testing import FlaskClient

from src import main


@pytest.fixture(scope="session")
def client() -> FlaskClient:
    with main.api.test_client() as client:
        yield client


@pytest.fixture(scope="session")
def authorized_auth() -> dict:
    return {"username": main.AUTH_USERNAME, "password": main.AUTH_PASSWORD}


@pytest.fixture(scope="session")
def unauthorized_auth() -> dict:
    return {"username": "foo", "password": "bar"}


@pytest.fixture(scope="session")
def authorized_header(authorized_auth: FixtureFunctionMarker) -> dict:
    return {
        "Authorization": _basic_auth_str(
            authorized_auth["username"], authorized_auth["password"]
        ),
    }


@pytest.fixture(scope="session")
def unauthorized_header(unauthorized_auth: FixtureFunctionMarker) -> dict:
    return {
        "Authorization": _basic_auth_str(
            unauthorized_auth["username"], unauthorized_auth["password"]
        ),
    }


@pytest.fixture(scope="session")
def token_endpoint(unauthorized_auth: FixtureFunctionMarker) -> str:
    return "/api/token"
