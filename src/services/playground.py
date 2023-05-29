from googleapiclient.discovery import build
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


SCOPES=[
        'https://www.googleapis.com/auth/classroom.courses', 
        'https://www.googleapis.com/auth/classroom.coursework.me',
        'https://www.googleapis.com/auth/classroom.courses.readonly',
        "https://www.googleapis.com/auth/forms.body"
]
PATH = '/Users/andriigerasymchuk/private-repositories/quiz_compiler/sdist/oauth-creds.json'



# SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
STORAGE = Storage('credentials.storage')

# Start the OAuth flow to retrieve credentials
def authorize_credentials():
# Fetch credentials from storage
    credentials = STORAGE.get()
# If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(PATH, scope=SCOPES)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials
credentials = authorize_credentials()

# Set up the necessary credentials
# credentials = service_account.Credentials.from_service_account_file(PATH, SCOPES)


credentials = Credentials.from_authorized_user_file(PATH, SCOPES)

        

# Build the Classroom API service
service = build('classroom', 'v1', credentials=credentials)
courses = service.courses().list().execute()

# Define the quiz form details
course_id = 'your_course_id'
title = 'Quiz Form'
description = 'This is a quiz form for the Google Classroom Quiz example.'
state = 'DRAFT'  # Other states: 'PUBLISHED' or 'DELETED'

# Define the quiz questions
questions = [
    {
        'question': 'What is the capital of France?',
        'choices': ['Paris', 'London', 'Berlin', 'Madrid'],
        'correct_choice': 0,
        'image_url': 'https://example.com/image1.jpg'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'choices': ['Venus', 'Mars', 'Jupiter', 'Saturn'],
        'correct_choice': 1,
        'image_url': 'https://example.com/image2.jpg'
    }
]

# Create the quiz form
quiz_form = {
    'title': title,
    'description': description,
    'state': state,
    'multipleChoiceQuestion': [
        {
            'question': question['question'],
            'choices': question['choices'],
            'correctChoice': question['correct_choice'],
            'media': [
                {
                    'url': question['image_url'],
                    'form': 'IMAGE'
                }
            ]
        }
        for question in questions
    ]
}



form_service = discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

# Create the coursework with the quiz form
coursework = {
    'title': title,
    'description': description,
    'workType': 'ASSIGNMENT',
    'state': state,
    'assigneeMode': 'ALL_STUDENTS',
    'assignment': {
        'studentWorkFolder': {
            'title': title
        },
        'quiz': quiz_form
    }
}

# Create the coursework using the Classroom API
coursework = service.courses().courseWork().create(courseId=course_id, body=coursework).execute()

print(f"Quiz form created with ID: {coursework['id']}")
form = form_service.forms().create(body=NEW_FORM).execute()
# form created
{'formId': '1NEy8mty_z1p54QgG30dsZd4w9M4_0rjNHhREjhaAVxM', 'info': {'title': 'Quickstart form', 'documentTitle': 'Untitled form'}, 'revisionId': '00000002', 'responderUri': 'https://docs.google.com/forms/d/e/1FAIpQLSdUyZP19nFT6OXSbaDjG2SXZxr9rQfXxqUrsp5J-c7IwNZ0Jw/viewform'}

NEW_QUESTION2 = {
    "requests": [{
        "createItem": {
            "item": {
                "title": "In what year did the United States land a mission on the moon?",
                "questionItem": {
                    "question": {
                        "required": True,
                        # "grading": {
                        #     "pointValue": 2,
                        #     "whenWrong": {
                        #         "text": "hint text goes here"
                        #     },
                        # },
                        
                        "textQuestion": {
                            "paragraph": False
                        },
                    },
                    # "image": {
                    #     "contentUri": "",
                    #     "sourceUri": "https://drive.google.com/file/d/0B1vVbP2sHgDwUFRiSHRWY3RzVkE/view?usp=share_link&resourcekey=0-cOJS9zt-_tSLvfT9RE6r1Q",
                    #     "altText": "image text",
                    #     "properties": {
                    #        "alignment": "CENTER",
                    #        "width": 520
                    #     }
                    # }
                },
            },
            "location": {
                "index": 1
            }
        }
    }]
}
quuestions = form_service.forms().batchUpdate(formId=form['formId'], body=NEW_QUESTION2).execute()