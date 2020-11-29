from one_piece_scan_bot.credentials import drive_client_id, drive_client_secret, drive_refresh_token
from one_piece_scan_bot.constants import DRIVE_SCOPES, DRIVE_TOKEN_URI

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


class DriveService:

    def __init__(self):
        credentials = Credentials(
            token=None,
            refresh_token=drive_refresh_token,
            token_uri=DRIVE_TOKEN_URI,
            client_id=drive_client_id,
            client_secret=drive_client_secret,
            scopes=DRIVE_SCOPES
        )
        self._service = build('drive', 'v3', credentials=credentials)

    @property
    def service(self):
        return self._service

    def list_files(self, parent_dir_id=None, q='', mime_type=None, page_token=None):
        if parent_dir_id:
            if q != '':
                q += ' and '
            q += f"'{parent_dir_id}' in parents"

        if mime_type:
            if q != '':
                q += ' and '
            q += f"mimeType='{mime_type}'"

        results = self.service.files().list(
            corpora='user',
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token,
            q=q,
        ).execute()
        page_token = results.get('nextPageToken')
        items = results.get('files', [])
        if not page_token:
            return items
        return items + self.list_files(parent_dir_id, q, mime_type, page_token)

    def create_file(self, name, mime_type, parent_dir_id=''):
        file_metadata = {
            'name': name,
            'mimeType': mime_type,
            'parents': [parent_dir_id]
        }
        return self.service.files().create(body=file_metadata).execute()
