

import logging
import os
from pathlib import Path
from src.services import StateMixin
from src.ast_parser import KNOWN_COMMENTS, Compiler, Lexer, Parser
from src.utils import create_image_from_multiline_text


logger = logging.getLogger(__name__)


class CodeGeneratorService(StateMixin):
    def __init__(self):
        super().__init__()
        self._state = None


    def compile_file(self, path: str | Path ) -> None:

        file_name = Path(os.path.basename(path))
        state_name = file_name.with_suffix('').name
        with open(path, 'r') as f:
            text = f.read()
            lexer = Lexer(text, comment_separator=KNOWN_COMMENTS[file_name.suffix.replace('.', '')])
            parser = Parser(lexer)
            compiler = Compiler(parser)
            compiler.compile()
            compiler.dump_state(state_name)
    
    def convert_code_image(self, state_name: str, key_name: str = 'code', ext='png', force: bool = False) -> None:
        """
        Operates on state["items"] and converts provided key_name to the image

        """
        key = f'{key_name}_image_path'
        for idx, item in enumerate(self.get_state(state_name)["items"]):
            item[key] = str(create_image_from_multiline_text(state_name, item[key_name], image_name=f'{key_name}_{idx}.{ext}'))
        self.dump_state(state_name)


