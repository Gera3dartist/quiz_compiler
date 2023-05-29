
from functools import partial
import logging
import os
from typing import MutableMapping
from googleapiclient.discovery import build, Resource
from oauth2client.client import OAuth2Credentials
from googleapiclient.http import MediaFileUpload


import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from pyparsing import Sequence
from src.services import StateMixin

logger = logging.getLogger(__name__)

SCOPES=[
        'https://www.googleapis.com/auth/classroom.courses', 
        'https://www.googleapis.com/auth/classroom.coursework.me',
        'https://www.googleapis.com/auth/classroom.courses.readonly',
        'https://www.googleapis.com/auth/forms.body',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.metadata',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.photos.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
]
PATH = '/Users/andriigerasymchuk/private-repositories/quiz_compiler/sdist/oauth-creds.json'

DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
STORAGE = Storage('credentials.storage')


def authorize_credentials() -> OAuth2Credentials:
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(PATH, scope=SCOPES)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


def get_form_service(credentials: OAuth2Credentials) -> Resource:
    return build('forms', 'v1', http=credentials.authorize(httplib2.Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)


def get_drive_service(credentials: OAuth2Credentials) -> Resource:
    return build('drive', 'v3', http=credentials.authorize(httplib2.Http()))


class GoogleWorkspaceService(StateMixin):
    def __init__(self, form_service: Resource, drive_service: Resource):
        super().__init__()

        self.form_service = form_service
        self.drive_service = drive_service
        self._state = None

    def maybe_create_form(self):
        body = {"info": {"title": self.metadata["topicTest"]}}
        return self.form_service.forms().create(body=body).execute()

    def populate_question(
            self, 
            title: str, 
            required: bool = False,
            # itemType: str = "textQuestion",
            image_uri: str = None,
            ) -> dict:

        base = {
                "title": title,
                "questionItem": {
                    "question": {
                        "required": required,
                        "textQuestion": {
                            "paragraph": False
                        },
                    },
                },
            }
        if image_uri:
            base["questionItem"]["image"] = {
                "contentUri": "",
                "sourceUri": image_uri,
                "altText": "image text",
                # "properties": {
                #     "alignment": "CENTER",
                # }
            }
        return base
    
    def populate_item(self, item: dict, index: int) -> dict:
        return {
            "createItem": {
                "item": item,
                "location": {
                    "index": index
                }}
            }
    
    def questions_from_state(self) -> Sequence[dict]:
        result = []
        for idx, question in enumerate(self.state["items"]):
            _question = question['question']
            _question.replace("\n", " ").replace("\r", " ")

            title = f"{_question}"
            title = title.replace("\n", " ").replace("\r", " ")

            image_drive_id = question.get('image_drive_id')
            
            image_data = {'image_uri': image_drive_id} if image_drive_id else {}
            result.append(
                self.populate_item(
                    item=self.populate_question(
                        title=title, **image_data), 
                    index=idx)
                )
        return result
    
    def update_form_with_questions(self, form_id: str) -> MutableMapping:
        body = {
            "requests": self.questions_from_state()
        }
        return self.form_service.forms().batchUpdate(formId=form_id, body=body).execute()
    
    def upload_image(self, path: str, folder_id: str) -> str:
        """
        Uploads image to the google drive and returns the link
        creates folder images if not exists
        """

        file_metadata = {'name': path.split(os.sep)[-1]}
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        media = MediaFileUpload(path, mimetype='image/png')
        file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='thumbnailLink').execute()
        return file.get('thumbnailLink')
    
    def maybe_create_folder_on_google_drive(self, folder_name: str) -> str:
        """
        Creates folder on google drive if not exists
        """
        folder_id = None
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        response = self.drive_service.files().list(q=query).execute()
        if len(response['files']) == 0:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = self.drive_service.files().create(body=file_metadata, fields='id').execute()
            folder_id = file.get('id')
        else:
            folder_id = response['files'][0]['id']
        return folder_id
    
    def upload_images_to_drive(self) -> None:
        folder_id = self.maybe_create_folder_on_google_drive('TestImages')
        for question in self.state["items"]:
            image_path = question['code_image_path']
            image_id = self.upload_image(image_path, folder_id)
            question['image_drive_id'] = image_id
        self.dump_state()
    
    def remove_images(self) -> None:
        """
        Removes images from the google drive by file id
        """
        for question in self.state["items"]:
            if image_id := question.get('image_drive_id'):
                logger.info('Removing image with id %s from drive', image_id)
                self.drive_service.files().delete(fileId=image_id).execute()
        