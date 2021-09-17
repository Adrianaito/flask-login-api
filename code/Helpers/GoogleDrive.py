import io
from googleapiclient.http import MediaIoBaseUpload, HttpError
import base64
from dotenv import load_dotenv
from os import environ

from .GoogleService import Create_Service

load_dotenv()

CLIENT_SECRET_FILE = environ["CLIENT_SECRET_FILE"]
API_NAME = environ["API_NAME"]
API_VERSION = environ["API_VERSION"]
# SCOPES = ["https://www.googleapis.com/auth/drive"]
SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.metadata.readonly"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


# ****************************** CREATE FOLDER **************************************


def create_drive_folder(folder_name):
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        # "parents": []
    }

    folder = service.files().create(body=file_metadata).execute()
    folder_id = folder.get("id")

    return folder_id

# ***********************************************************************************


# ****************************** UPLOAD FILES **************************************

def upload_google_drive(file_name: str,
                        pdf_bytes: bytes,
                        folder_id: str = None,
                        extension="pdf",
                        mime_type="application/pdf"
                        ) -> str:

    file_name_with_extension = f"{file_name}.{extension}"

    file_metadata = {
        "name": file_name,
        # "parents": [folder_id]
    }
    fh = io.BytesIO(pdf_bytes)
    media = MediaIoBaseUpload(
        fh, mimetype=mime_type)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    file_id = file.get('id')

    return file_id

# ***********************************************************************************

# ****************************** DOWNLOAD FILES **************************************


def download_from_drive(file_id: str) -> str:

    request = service.files().get_media(fileId=file_id)
    response = request.execute()
    encoded = base64.b64encode(response)
    pdf_string = encoded.decode("utf-8")
    print("from google")

    return pdf_string


# ***********************************************************************************

# ****************************** DELETE FILES **************************************

def delete_drom_drive(fileId):
    try:
        service.files().delete(fileId=fileId).execute()
        return ({"message": "Success!", "valid": True}, 200)
    except HttpError as e:
        print("error", e)
        return ({"message": "File not Found!", "valid": False}, 404)
