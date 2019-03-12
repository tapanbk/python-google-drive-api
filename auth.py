from __future__ import print_function
import pickle
import os.path
from google.auth.transport.requests import Request

from google_auth_oauthlib.flow import InstalledAppFlow


class Auth:
    def __init__(self, SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME

    def get_credentials(self):
        cwd = os.getcwd()
        credential_dir = os.path.join(cwd, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'credentials.json')
        credential_token = os.path.join(credential_dir, 'token.pickle')
        creds = None
        if os.path.exists(credential_token):
            with open(credential_token, 'rb') as token:
                creds = pickle.load(token)
                print(creds)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_path, self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(credential_token, 'wb') as token:
                pickle.dump(creds, token)
        return creds
