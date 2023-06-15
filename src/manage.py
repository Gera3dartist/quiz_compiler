
import os
from pathlib import Path
import click
from dependency_injector.wiring import inject, Provide


from src.constants import FORM_ID
from src.container import ApplicationContainer as Container
from src.services.compiler import CodeGeneratorService
from src.services.google_workspace import GoogleWorkspaceService, authorize_credentials
from src.utils import get_build_directory

@click.group()
def cli():
    """CLI tool for performing various operations."""
    pass


@click.command()
@click.option('--path', help='Path to mpt definition file')
@inject
def compile(
    path: str | bytes, 
    compiler_service: CodeGeneratorService = Provide[Container.compiler_service],
    google_service: GoogleWorkspaceService = Provide[Container.google_service]
    ):
    """Opens file and compiles it"""
    # get name of the file from path
    state_name = Path(os.path.basename(path)).with_suffix('').name

    # check that state for this file already exists
    if f'{state_name}.json' in os.listdir(get_build_directory()):
        try:
            google_service.remove_images(state_name)
        except Exception as e:
            print(e)
            print('Failed to remove images from google drive')

    compiler_service.compile_file(path)
    compiler_service.convert_code_image(state_name)
    google_service.upload_images_to_drive(state_name)


@click.command()
@inject
def show_state():
    """Displays state of the application"""
    print('Showing available states')
    for state  in (f for f in os.listdir(get_build_directory()) if f.endswith('.json')):
        print(f"\t - {state.replace('.json', '')}")


@click.command()
@inject
def create_form(google_service: GoogleWorkspaceService = Provide[Container.google_service]):
    """Displays state of the application"""
    result = google_service.maybe_create_form()
    print(result)
   

@click.command()
@inject
@click.option('--form_id', help='Id of the form to update', default=FORM_ID)
@click.option('--state_name', help='name of the state to use', default='state')
def upload_to_google(form_id: str, state_name: str,  google_service: GoogleWorkspaceService = Provide[Container.google_service]):
    """Displays state of the application"""
    print('FORM_ID: %s' % form_id)
    if not os.path.exists(get_build_directory() / f'{state_name}.json'):
        raise ValueError(f"State {state_name} does not exist")

    result = google_service.update_form_with_questions(form_id, state_name)
    print(result)


@click.command()
@inject
def google_login():
    print('Logging in to google - Started')
    authorize_credentials()
    print('Logging in to google - Success')


# TODO:
# 1. Create form per variant

cli.add_command(compile)
cli.add_command(upload_to_google)
cli.add_command(show_state)
cli.add_command(create_form)
cli.add_command(google_login)


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    cli()