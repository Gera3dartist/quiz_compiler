

import logging
from click import Path
from src.services import StateMixin
from src.ast_parser import Compiler, Lexer, Parser
from src.utils import create_image_from_multiline_text
from googleapiclient.discovery import Resource


logger = logging.getLogger(__name__)


class CompilerService(StateMixin):
    def __init__(self, drive_service: Resource):
        super().__init__()
        self._state = None
        self.drive_service = drive_service


    def compile_file(self, path: str | Path ) -> None:
        with open(path, 'r') as f:
            text = f.read()
            lexer = Lexer(text)
            parser = Parser(lexer)
            compiler = Compiler(parser)
            compiler.compile()
            compiler.dump_state()
    
    def convert_code_image(self, key_name: str = 'code', ext='png', force: bool = False) -> None:
        """
        Operates on state["items"] and converts provided key_name to the image

        """
        key = f'{key_name}_image_path'
        for idx, item in enumerate(self.state["items"]):
            item[key] = str(create_image_from_multiline_text(item[key_name], image_name=f'{key_name}_{idx}.{ext}'))
        self.dump_state()


