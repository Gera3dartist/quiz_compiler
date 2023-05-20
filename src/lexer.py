
from enum import Enum
import typing as t
import operator

keywords = {
    'course': 'COURSE',
    'programLanguage': 'PROGRAM_LANGUAGE',
    'topicTest': 'TOPIC_TEST',
    'date': 'DATE',
}


class TokenTypes(Enum):
    INTEGER = 'INTEGER'
    OPERATOR = 'OPERATOR'
    EOF = 'EOF'

OPERATIONS = {
    '/': lambda a,b: float(a)/b,
    '*': lambda a,b: a * b,
    '+': lambda a,b: a + b,
    '-': lambda a,b: a - b,
}


class Token:
    def __init__(self, a_type, value):
        self.value = value
        self.type = a_type

    def __repr__(self):
        return f"Token: {self.type}, {self.value}"

class Lexer:
    """
    Get program text and returns a list of know tokens
    """
    def __init__(self, program_text: str) -> None:
        self.pos = 0
        self.text = program_text
        self.current_token = None

    def get_char(self) -> t.Optional[str]:
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def parse_integer(self, value: str) -> int:
        digits = []
        while (value := self.get_char()) and value and value.isdigit():
            digits.append(value)
            self.advance()
        return int(''.join(digits))
    
    def parse_buffer(self, buffer: t.List[str]) -> Token:
        value = ''.join(buffer)
        if value in KNOWN_COMMENTS:
            return Token(TokenTypes.INTEGER, self.parse_integer(value))
        elif value in OPERATIONS:
            return Token(TokenTypes.OPERATOR, value)
        else:
            raise ValueError(f"Unexpected token: {value}"
        

    def advance(self):
        self.pos += 1
    
    def get_next_token(self):
        """
        Goes over program text and yields list of tokens
        """
        buffer = []
        should_parse = False
        while True:
            current_char = self.get_char()

            if current_char is None:
                return Token(TokenTypes.EOF, None)
            elif should_parse and buffer:
                token = self.parse_buffer(buffer)
                should_parse = False
                buffer = []
                return token

            elif current_char.isspace():
                self.advance()
                should_parse = True
        
            else:
                raise ValueError(f"Not supported token: {current_char}")
            
    def eat(self, token: Token, category: TokenTypes):
        assert token.type == category
    
    def add_to_stack(self, value: Token, stack: t.List):
        print (f"adding to stack: {value.value}")
        stack.append(value)
        print(f"stack: {stack}")

    def expr(self):
        """
        Expr = INT Op INT
        Op  = + | - | * | / 
        """
        stack = []
        lhs = self.get_next_token()
        self.eat(lhs, TokenTypes.INTEGER)
        self.add_to_stack(lhs, stack)
        while True:
            current_token = self.get_next_token()

            if current_token.type == TokenTypes.EOF:
                break
            elif current_token.type == TokenTypes.INTEGER:
                op = stack.pop()
                self.eat(op, TokenTypes.OPERATOR)
                initial = stack.pop()
                self.eat(initial, TokenTypes.INTEGER)

                self.add_to_stack(
                    value=Token(TokenTypes.INTEGER, OPERATIONS[op.value](initial.value, current_token.value)),
                    stack=stack
                )
            elif current_token.type == TokenTypes.OPERATOR:
                self.add_to_stack(current_token, stack)
            else:
                raise ValueError(f"Unexpected token: {current_token}")

        return stack.pop().value
    
    def parse_metadata(self):
        """
        Metadata = Course, ProgramLanguage, TopicTest, Date, Annonce;
        """
        self.parse_course()
        self.parse_program_language()
        self.parse_topic_test()
        self.parse_date()
        self.parse_annonce()

        pass
    def parse_questions(self):
        pass

        


        
def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        print(lexer.expr())


if __name__ == '__main__':
    main()