from enum import Enum
import itertools
from pathlib import Path
import typing as t

from src.utils import get_build_directory


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
KNOWN_BLOCKS_DIVIDERS = {
    'beginAnnonce': 'endAnnonce',
    '?begin': '?end',
    '!begin': '!end',
    'beginHint': 'endHint',
    'beginCode': 'endCode'
}

KNOWN_ITEM_DIVIDERS = {
    'newQuestion': 'endQuestion',
}


def get_block_name(block: str) -> str:
    return {
        'beginAnnonce' : 'announce',
        'newQuestion' : 'item',
        'beginHint' : 'hint',
        'beginCode' : 'code',
        '!begin' : 'answer',
        '?begin' : 'question',
    }.get(block, block)


KEY_SEPARATOR = ':'


class TokenTypes(Enum):
    KEY = 'KEY'
    VALUE = 'VALUE'
    BLOCK_START = 'BLOCK_START'
    BLOCK_END = 'BLOCK_END'
    META_COMMENT = 'META_COMMENT'
    KEY_SEPARATOR = 'KEY_SEPARATOR'
    EOF = 'EOF'
    ITEM_START = 'ITEM_START'
    ITEM_END = 'ITEM_END'



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


class ASTNode:
    pass


class BinOp(ASTNode):
    def __init__(self, left: ASTNode, op: Token, right: ASTNode):
        self.left = left
        self.token = op
        self.op = op
        self.right = right

    def __repr__(self) -> str:
        return f"BinOp({self.left}, {self.op}, {self.right})"
    def __eq__(self, __value: object) -> bool:
        return self.left == __value.left and self.op == __value.op and self.right == __value.right

class Key(ASTNode):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"KeyWord({self.token})"
    
    def __eq__(self, __value: object) -> bool:
        return self.token.value == __value.token.value and self.token.type == __value.token.type

class Value(ASTNode):
    def __init__(self, token: Token):
        self.token = token
        self.value = token.value

    def __repr__(self) -> str:
        return f"Value({self.token})"
    
    def __eq__(self, __value: object) -> bool:
        return self.token.value == __value.token.value and self.token.type == __value.token.type


class Compound(ASTNode):
    def __init__(self, name: str = None):
        self.name = name
        self.children = []

    def __repr__(self) -> str:
        return f"Compound(name={self.name},children={self.children})"
    
    def append(self, node: ASTNode):
        self.children.append(node)

    def add_children(self, children: list[ASTNode]) -> ASTNode:
        self.children.extend(children)
        return self
    
    def __iter__(self):
        return iter(self.children)
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name and self.children == __value.children


class Empty(ASTNode):
    pass



###############################################################################
#                                                                             #
#  LEXER                                                                      #
#                                                                             #
###############################################################################


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
            chars.append(self.current_charachter)
            self.advance()
        value = ''.join(chars).strip()
        return Token(TokenTypes.VALUE, value)


    def parse_token(self) -> t.Optional[Token]:
        """
        Joined sequence of characters till whitespace
        """
        chars = []
        
        # get chunk of text till whitespace
        while self.current_charachter not in {None, ' ', KEY_SEPARATOR, *LINE_BREAKS}:
            chars.append(self.current_charachter)
            self.advance()
        
        word = ''.join(chars)

        if word in KNOWN_KEYWORDS:
            return Token(TokenTypes.KEY, word)
        
        # parse block token
        elif word in KNOWN_ITEM_DIVIDERS:
            return Token(TokenTypes.ITEM_START, word)
        elif word in KNOWN_ITEM_DIVIDERS.values():
            return Token(TokenTypes.ITEM_END, word)
        elif word in KNOWN_BLOCKS_DIVIDERS:
            return Token(TokenTypes.BLOCK_START, word)
        elif word in KNOWN_BLOCKS_DIVIDERS.values():
            return Token(TokenTypes.BLOCK_END, word)
            
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
            if self.current_charachter.isspace():
                self.skip_whitespace()
            elif self.current_charachter in LINE_BREAKS:
                self.advance()
            # handle meta comments
            elif self.current_charachter in META_COMMENT and (meta_comment := self.parse_meta_comment()):
                self.advance()
                # return Token(TokenTypes.META_COMMENT, meta_comment)
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


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################


class Parser:
    """
    Operates on tokens, ensures semantic correctness
    """
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, _type: TokenTypes):
        if self.current_token.type == _type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ValueError(f"Expected {_type} got {self.current_token.type} value: {self.current_token.value}")

    def parse_value(self) -> Value:
        """
        Parse value
        """
        values = []
        while (value := self.current_token).type == TokenTypes.VALUE:
            self.eat(TokenTypes.VALUE)
            values.append(value.value) # if many lines - join them
        result = '\n'.join(values) if len(values) > 1 else values[0]
        
        return Value(Token(TokenTypes.VALUE, result))
    
    def key_value(self) -> ASTNode:
        """
        KEY : VALUE, {VALUE}
        """
        key = self.current_token
        self.eat(TokenTypes.KEY)
        operation = self.current_token
        self.eat(TokenTypes.KEY_SEPARATOR)
        
        return BinOp(left=Key(key), op=operation, right=self.parse_value())
    
    def error(self):
        raise ValueError(f"Invalid token: {self.current_token}")
    
    def item(self, block_name: str = None) -> ASTNode:
        """
        block_start, Statement, {Statement}, block_end
        """
        starting_block = self.current_token
        if block_name and block_name != starting_block.value:
            self.error()
        
        self.eat(TokenTypes.ITEM_START)
        # inside of the block correct constuctions are:
        # 1. key value pairs
        # 2. block
        # 3. meta comment
        # 4. value
        nodes: list[ASTNode] = self.statement_list()

        self.eat(TokenTypes.ITEM_END)
        root = Compound(name=get_block_name(starting_block.value))
        for node in nodes:
            root.append(node)
        return root
    

    def block(self, block_name: str = None) -> ASTNode:
        """
        block inside item parsed as key and value
        """
        starting_block = self.current_token
        if block_name and block_name != starting_block.value:
            self.error()
        
        self.eat(TokenTypes.BLOCK_START)
    
        value = self.parse_value()

        self.eat(TokenTypes.BLOCK_END)
        return BinOp(
            left=Key(Token(TokenTypes.KEY, get_block_name(starting_block.value))), 
            op=Token(TokenTypes.KEY_SEPARATOR, KEY_SEPARATOR), 
            right=value
        )
        
    
    def metacomment(self) -> None:
        """
        metacomment = META_COMMENT, {META_COMMENT}
        """
        while self.current_token.type == TokenTypes.META_COMMENT:
            self.eat(TokenTypes.META_COMMENT)

    
    def statement(self) -> ASTNode | None:
        """
        statement = (ASSIGNMENT|CODE_BLOCK|VALUE|METACOMMENT)
        """
        if self.current_token.type == TokenTypes.META_COMMENT:
            return self.metacomment()  # retuns None
        elif self.current_token.type == TokenTypes.KEY:
            return self.key_value()
        elif self.current_token.type == TokenTypes.BLOCK_START:
            return self.block()
        elif self.current_token.type == TokenTypes.VALUE: 
            return self.parse_value()
        else:
            self.error()
    
    def statement_list(self) -> list[ASTNode]:
        """
        statement = (ASSIGNMENT|CODE_BLOCK|VALUE), {ASSIGNMENT|CODE_BLOCK|VALUE}
        """
        results = []
        while self.current_token.type not in (TokenTypes.ITEM_END, TokenTypes.EOF):
            if statement := self.statement():
                results.append(statement)
        if not results:
            return [Empty()]
        return results  
    
    def metainfo(self) -> ASTNode:
        """
        metainfo = META_COMMENT, {META_COMMENT}
        """
        meta = Compound('metadata')
        while self.current_token.type in {TokenTypes.KEY, TokenTypes.META_COMMENT}: #, TokenTypes.VALUE, TokenTypes.KEY_SEPARATOR):
            meta.append(self.statement())
        return meta


    def program(self) -> ASTNode:
        """
        program = metainfo, block, {block}
        """
        root = Compound('program')
        root.append(self.metainfo())

        while self.current_token.type != TokenTypes.EOF:
            if self.current_token.type == TokenTypes.ITEM_START:
                root.append(self.item())
            elif self.current_token.type == TokenTypes.BLOCK_START:
                root.append(self.block())
        return root

    def parse(self) -> ASTNode:
        return self.program()



###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node: ASTNode):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Compiler(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.curent_children = {}
        self.state = {
            'metadata': None,
            'announce': None,
            'items': [],

        }

    def visit_BinOp(self, node):
        if node.op.type == TokenTypes.KEY_SEPARATOR:
            if node.left.value in self.state:
                self.state[node.left.value] = node.right.value
            else:
                self.curent_children[node.left.value] = self.visit(node.right)

    def visit_Key(self, node):
        return node.value
    
    def visit_Value(self, node):
        return node.value
    
    def visit_Compound(self, node):
        """
        compound should be added to propper place in state
        """
        
        for child in node.children:
            self.visit(child)
        if self.curent_children and node.name in self.state:
            # populate state
            self.state[node.name] = self.curent_children
            self.curent_children = {}
        elif node.name == 'item':
            self.state['items'].append(self.curent_children)
            self.curent_children = {}

    def compile(self) -> Key | Value | Compound | BinOp | None:
        tree = self.parser.parse()
        return self.visit(tree)
    
    def dump_state(self) -> None:
        """
        Dumps state to json file lacated in directory where build is
        """
        import json
        with open(get_build_directory() / 'state.json', 'w') as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
