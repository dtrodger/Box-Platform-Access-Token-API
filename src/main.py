"""
Box Platform access token API
"""
import logging.config
import os
from typing import Tuple, Union

from flask import (
    Flask,
    request,
    jsonify,
    Response
)
import requests
import yaml
import boxsdk
import click


log = logging.getLogger(__name__)


AUTH_ENDPOINT = "http://127.0.0.1:5000/api/token"
AUTH_USERNAME = "dave"
AUTH_PASSWORD = "Welcome2020"
BOX_JWT_KEYS_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "box_jwt_keys.yml"
)
USER_STORE = {AUTH_USERNAME: AUTH_PASSWORD}
api = Flask(__name__)
box_jwt_keys = None


def configure_logging() -> None:
    """
    Configure INFO level logging to stdout
    """
    logging.basicConfig(level=logging.INFO)
    box_sdk_log = logging.getLogger("boxsdk")
    box_sdk_log.setLevel(logging.ERROR)


def get_box_platform_access_token() -> str:
    """
    Box SDK access token generation helper
    """
    global box_jwt_keys
    if not box_jwt_keys:
        with open(BOX_JWT_KEYS_FILE_PATH, "r") as fh:
            box_jwt_keys = yaml.load(fh, Loader=yaml.FullLoader)

    box_auth = boxsdk.JWTAuth.from_settings_dictionary(box_jwt_keys)
    box_auth.authenticate_instance()

    return box_auth.access_token


def validate_username_password(
        username: Union[str, None],
        password: Union[str, None]
) -> bool:
    """
    Validates a username and password against the user store
    """
    valid = False
    if (
        username
        and password
        and username in USER_STORE.keys()
        and USER_STORE.get(username) == password
    ):
        valid = True

    return valid


@api.route("/api/token", methods=["GET"])
def token() -> Tuple[Response, int]:
    """
    Box Platform access token generation endpoint
    """
    try:
        auth_username = request.authorization.get("username")
        auth_password = request.authorization.get("password")
        if validate_username_password(auth_username, auth_password):
            resp_code = 200
            resp_body = {"access_token": get_box_platform_access_token()}
        else:
            resp_code = 401
            resp_body = {"message": "Unauthorized"}
    except Exception as e:
        log.error(f"token request failed with {e}")
        resp_code = 500
        resp_body = {"message": "Internal server error"}

    return jsonify(resp_body), resp_code


@click.group()
def cli() -> None:
    """
    Click group for multiple commands
    """


@click.command()
def runserver() -> None:
    """
    CLI command to run the API
    """
    configure_logging()
    api.run()


@click.command()
def callserver() -> None:
    """
    HTTP client CLI command
    """
    configure_logging()
    response = requests.get(AUTH_ENDPOINT, auth=(AUTH_USERNAME, AUTH_PASSWORD))
    log.info(response.status_code)
    log.info(response.content)


def main() -> None:
    """
    Configure the CLI commands to a click group
    """
    commands = [
        callserver,
        runserver
    ]
    for command in commands:
        cli.add_command(command)

    cli()


if __name__ == "__main__":
    main()
