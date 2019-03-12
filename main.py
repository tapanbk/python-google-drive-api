from __future__ import print_function

import io
import  mimetypes
from apiclient import errors
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import auth

SCOPES = ['https://www.googleapis.com/auth/drive']
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Drive APi Python Quickstart'
authInstant = auth.Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInstant.get_credentials()
drive_service = build('drive', 'v3', credentials=credentials)


def list_files(size):
    """ List all files of the drive"""
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name, trashed)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['trashed']))


def upload_file(file_name):
    """ Upload file to  a root folder of a drive"""
    file_path = 'files/'+str(file_name)
    file_metadata = {'name': file_name}
    mime_type = get_file_mime_type(file_name)
    media = MediaFileUpload(file_path,
                            mimetype=mime_type)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def get_file_mime_type(file_name):
    """ Get file mime_type"""
    mime_type = mimetypes.guess_type(file_name)
    if mime_type:
        mime_type = mime_type[0]
    else:
        mime_type = None
    return mime_type


def download_file(file_id, file_path):
    """ Download file from the drive"""
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    with io.open(file_path, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def create_folder(folder_name):
    """ Create a new folder """
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = drive_service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % file.get('id'))


def upload_file_to_folder(folder_id, file_name):
    """Upload file to a folder """

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    mime_type = get_file_mime_type(file_name)
    file_path = 'files/'+str(file_name)
    media = MediaFileUpload(file_path,
                            mimetype=mime_type,
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print('File ID: %s' % file.get('id'))


def search_file(size):
    """search file in a drive """

    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name, trashed)",q="name contains '1.jpg' and trashed =0").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1}) - {2}'.format(item['name'], item['id'], item['trashed']))


def get_file_inside_folder(size, parent_id):
    """get all files in a inside a folder  """

    query = "parents='{}'".format(parent_id)
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)", q=query).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def search_file_inside_folder(size, parent_id):
    """search file in a inside a folder  """

    query = "name contains 'jpg' and parents='{}'".format(parent_id)
    results = drive_service.files().list(
        pageSize=size, fields="nextPageToken, files(id, name)",q=query).execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def delete_file(file_id):
    """Delete file permanently from drive."""
    try:
        return drive_service.files().delete(fileId=file_id).execute()
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


def empty_trash():
    """Empty all files from drive trash."""
    drive_service.files().emptyTrash().execute()


# list_files(100)
# upload_file('1.JPG')
# download_file('117jlp_pOjnbUUe9izMRT1KaXehFzjw3K', 'newfile.jpg')
# create_folder('New Test/sdfds')
# upload_file_to_folder('15EAQWRY0xSoNNi2LVRLScRcORpbK8CC9', '1.JPG')
# search_file(100)
# get_file_inside_folder(100,'15EAQWRY0xSoNNi2LVRLScRcORpbK8CC9')
# delete_file('1n6tkXGa5gaWrsqkFc-g-dzeXM2EA0wdn')
# empty_trash()
