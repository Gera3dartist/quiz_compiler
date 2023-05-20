from enum import Enum
import itertools
import typing as t


ASSIGN = 'ASSIGN'
META_COMMENT = '---'
KNOWN_COMMENTS = {
    'haskell': '--', 
    'c': '//', 
    'python': '#'
}

LINE_BREAKS = {'\n', '\r', '\r\n', '\n\r'}
KNOWN_KEYWORDS = {
    'course',
    'programLanguage',
    'topicTest',
    'date',
    'itemType'
}
KNOWN_BLOCKS = (
    ('beginAnnonce', 'endAnnonce'),
    ('?begin', '?end'),
    ('!begin', '!end'),
    ('beginHint', 'endHint'),
    ('beginCode', 'endCode'),
    ('newQuestion', 'endQuestion'),
)

KNOWN_BLOCKS_FLAT = set(itertools.chain.from_iterable(KNOWN_BLOCKS))

KEY_SEPARATOR = ':'


class TokenTypes(Enum):
    KEY = 'KEY'
    VALUE = 'VALUE'
    BLOCK = 'BLOCK'
    META_COMMENT = 'META_COMMENT'
    # BLOCK_START = 'BLOCK_START'
    # BLOCK_END = 'BLOCK_END'
    KEY_SEPARATOR = 'KEY_SEPARATOR'
    EOF = 'EOF'



def is_comment(char: str, comment_type: str) -> bool:
    return KNOWN_COMMENTS[comment_type][0] == char


class Token:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value})"
    
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value and self.type == __value.type


class AST:
    pass


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = op
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Key(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"KeyWord({self.token})"

class Value(AST):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"Value({self.token})"

class Lexer:
    def __init__(self, text: str, comment_separator=KNOWN_COMMENTS['haskell']) -> None:
        self.text = text
        self.pos = 0
        self.current_charachter = self.text[self.pos]
        self.comment_separator = comment_separator
    
    def error(self):
        raise ValueError("Invalid character")
    
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_charachter = None
        else:
            self.current_charachter = self.text[self.pos]
    
    def parse_value(self, initial_value: str = ''):
        """
        Parse value
        """
        chars = [*initial_value]
        # get everything till line break
        while self.current_charachter  not in {None, *LINE_BREAKS}:
            print(f'parse_value current: {self.current_charachter} pos: {self.pos}')
            chars.append(self.current_charachter)
            self.advance()
        value = ''.join(chars).strip()
        # value = value.replace("\'", "\'") # escape single quotes
        # value = value.replace("\"", '\\"') # escape double quotes
        print(f'value: {value}')
        return Token(TokenTypes.VALUE, ''.join(chars).strip())


    def parse_token(self) -> t.Optional[Token]:
        """
        Joined sequence of characters till whitespace
        """
        chars = []
        
        # get chunk of text till whitespace
        while self.current_charachter not in {None, ' ', KEY_SEPARATOR, *LINE_BREAKS}:
            print(f'current: {self.current_charachter} pos: {self.pos}')
            chars.append(self.current_charachter)
            self.advance()
        
        word = ''.join(chars)

        if word == 'endQuestio':
            print('endQuestion')
        print(f'word: {word}')
        if word in KNOWN_KEYWORDS:
            return Token(TokenTypes.KEY, word)
        
        # parse block token
        elif word in KNOWN_BLOCKS_FLAT:
            return Token(TokenTypes.BLOCK, word)
            
        elif word:
            # means not known keywords found - everything till line break is value
            return self.parse_value(word)
        else:
            self.error()

    def skip_whitespace(self):
        while self.current_charachter is not None and self.current_charachter.isspace():
            self.advance()

    def parse_meta_comment(self) -> str:
        """
        Skip the line if metacomment
        """
        chars = []
        meta_comment_length = len(META_COMMENT)
        meta_comment = self.text[self.pos:(self.pos+meta_comment_length)]
        if meta_comment == META_COMMENT:
            while self.current_charachter is not None:
                if self.current_charachter in LINE_BREAKS:
                    break
                chars.append(self.current_charachter)
                self.advance()
        return ''.join(chars).strip()

    def get_next_token(self) -> Token:
        while self.current_charachter != None:
            print(f'current: {self.current_charachter}')
            if self.current_charachter.isspace():
                self.skip_whitespace()
            elif self.current_charachter in LINE_BREAKS:
                self.advance()
            # handle meta comments
            elif self.current_charachter in META_COMMENT and (meta_comment := self.parse_meta_comment()):
                return Token(TokenTypes.META_COMMENT, meta_comment)
            elif self.current_charachter in self.comment_separator:
                # fast forward till in comment lexeme
                while self.current_charachter == self.comment_separator[0]:
                    self.advance()
                # here we know that some set of tokens will follow
            elif self.current_charachter == KEY_SEPARATOR:
                token = Token(TokenTypes.KEY_SEPARATOR, self.current_charachter)
                self.advance()
                return token
            # meaning we're parsing some word
            else:
                return self.parse_token()
        return Token(TokenTypes.EOF, None)
                






