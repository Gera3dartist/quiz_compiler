from collections import defaultdict
import json
import pprint
import click
from dependency_injector.wiring import inject, Provide

from src.ast_parser import Lexer, Parser, Compiler
from src.constants import FORM_ID
from src.container import ApplicationContainer as Container
from src.services.compiler import CompilerService
from src.services.google_workspace import GoogleWorkspaceService

@click.group()
def cli():
    """CLI tool for performing various operations."""
    pass


@click.command()
@click.option('--path', help='Path to mpt definition file')
@inject
def compile(
    path: str | bytes, 
    compiler_service: CompilerService = Provide[Container.compiler_service],
    google_service: GoogleWorkspaceService = Provide[Container.google_service]
    ):
    """Opens file and compiles it"""
    google_service.remove_images()
    compiler_service.compile_file(path)
    compiler_service.convert_code_image()
    google_service.upload_images_to_drive()



@click.command()
@inject
def check_state(google_service: GoogleWorkspaceService = Provide[Container.google_service]):
    """Displays state of the application"""
    print('SHOWING STATE')
    for q in google_service.questions_from_state():
        pprint.pprint(q)


@click.command()
@inject
def create_form(google_service: GoogleWorkspaceService = Provide[Container.google_service]):
    """Displays state of the application"""
    result = google_service.maybe_create_form()
    print(result)
   

@click.command()
@inject
@click.option('--form_id', help='Id of the form to update', default=FORM_ID)
def upload_to_google(form_id: str,  google_service: GoogleWorkspaceService = Provide[Container.google_service]):
    """Displays state of the application"""
    print('FORM_ID: %s' % form_id)

    result = google_service.update_form_with_questions(form_id)
    print(result)


cli.add_command(compile)
cli.add_command(upload_to_google)
cli.add_command(check_state)
cli.add_command(create_form)


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    cli()