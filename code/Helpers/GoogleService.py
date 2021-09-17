import pickle
import hashlib
import os
import webbrowser
import re
import socket
import sys
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime

_PORT = 8080
_REDIRECT_URI = f"http://localhost:{_PORT}/"


def Create_Service(client_secret_file, api_name, api_version, *scopes):

    # print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    # print("Scopes",SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print("pickle", pickle_file)

    if os.path.exists(pickle_file):
        print("Loading credentials from file...")
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
            print("existing cred", cred.to_json())

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            print("refresh token", cred.refresh_token)
            cred.refresh(Request())

        else:
            print("Fetching new tokens...")

            flow = Flow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)

            flow.redirect_uri = _REDIRECT_URI

            passthrough_val = hashlib.sha256(os.urandom(1024)).hexdigest()

            authorization_url, state = flow.authorization_url(access_type='offline',
                                                              include_granted_scopes='true',
                                                              prompt="consent",
                                                              state=passthrough_val)
            webbrowser.open(authorization_url)
            # print("Paste this URL into your browser: ")
            # print(authorization_url)
            print(
                f"\nWaiting for authorization and callback to: {_REDIRECT_URI}...")

            code = _get_authorization_code(passthrough_val)
            flow.fetch_token(code=code)
            cred = flow.credentials
            refresh_token = flow.credentials.refresh_token

            print(f"\nYour refresh token is: {refresh_token}\n")

            # flow = InstalledAppFlow.from_client_secrets_file(
            #     CLIENT_SECRET_FILE, SCOPES)

            # # flow.redirect_uri = 'http://localhost:8080/'
            # flow.authorization_url(access_type='offline',
            #                        include_granted_scopes='true')
            # flow.run_local_server(
            #     host="localhost", port=8080, open_browser=True, prompt="consent", authorization_prompt_message="")
            # cred = flow.credentials
            # print(cred.to_json())

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
        with open(pickle_file, 'rb') as token:
            t = pickle.load(token)
            print("new cred", t.to_json())
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        # print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def _get_authorization_code(passthrough_val):
    """Opens a socket to handle a single HTTP request containing auth tokens.
    Args:
        passthrough_val: an anti-forgery token used to verify the request
            received by the socket.
    Returns:
        a str access token from the Google Auth service.
    """
    # Open a socket at localhost:PORT and listen for a request
    sock = socket.socket()
    sock.bind(('localhost', _PORT))
    sock.listen(1)
    connection, address = sock.accept()
    data = connection.recv(1024)
    # Parse the raw request to retrieve the URL query parameters.
    params = _parse_raw_query_params(data)

    try:
        if not params.get("code"):
            # If no code is present in the query params then there will be an
            # error message with more details.
            error = params.get("error")
            message = f"Failed to retrieve authorization code. Error: {error}"
            raise ValueError(message)
        elif params.get("state") != passthrough_val:
            message = "State token does not match the expected state."
            raise ValueError(message)
        else:
            message = "Authorization code was successfully retrieved."
    except ValueError as error:
        print(error)
        sys.exit(1)
    finally:
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html\n\n"
            f"<b>{message}</b>"
            "<p>Please check the console output.</p>\n"
        )

        connection.sendall(response.encode())
        connection.close()

    return params.get("code")


def _parse_raw_query_params(data):
    """Parses a raw HTTP request to extract its query params as a dict.
    Note that this logic is likely irrelevant if you're building OAuth logic
    into a complete web application, where response parsing is handled by a
    framework.
    Args:
        data: raw request data as bytes.
    Returns:
        a dict of query parameter key value pairs.
    """
    # Decode the request into a utf-8 encoded string
    decoded = data.decode("utf-8")
    # Use a regular expression to extract the URL query parameters string
    match = re.search("GET\s\/\?(.*) ", decoded)
    params = match.group(1)
    # Split the parameters to isolate the key/value pairs
    pairs = [pair.split("=") for pair in params.split("&")]
    # Convert pairs to a dict to make it easy to access the values
    return {key: val for key, val in pairs}


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
