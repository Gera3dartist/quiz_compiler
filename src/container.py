"""
Uses python dependency injection to create a container for the application.
"""
from dependency_injector import containers, providers
from oauth2client.client import OAuth2Credentials
from src.services.compiler import CodeGeneratorService


from src.services.google_workspace import (
    GoogleWorkspaceService, 
    authorize_credentials, 
    get_form_service,
    get_drive_service,
)

class ApplicationContainer(containers.DeclarativeContainer):
    # config = providers.Configuration(yaml_files=['config.yml'])
    # Credentials
    # config_storage = providers.Singleton(

    credentials: OAuth2Credentials = providers.Singleton(authorize_credentials)

    # Services
    form_service = providers.Singleton(
        get_form_service, credentials=credentials
    )
    drive_service = providers.Singleton(
        get_drive_service, credentials=credentials)

    google_service: GoogleWorkspaceService = providers.Singleton(
        GoogleWorkspaceService, 
        form_service=form_service,
        drive_service=drive_service)
    
    compiler_service = providers.Resource(CodeGeneratorService)
