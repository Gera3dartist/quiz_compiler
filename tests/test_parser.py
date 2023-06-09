from src.ast_parser import Compound, Compiler, Lexer, Token, TokenTypes, Parser, Value, Key, BinOp

def test_lexer_parse_metadata():
    metadata = """
-- course: Functional Programming
-- programLanguage: Haskell
-- topicTest:  Standard types
-- date: 2023.03.09
"""
   
   

    lexer = Lexer(metadata)
    parser = Parser(lexer)
    metainfo = parser.metainfo()
    assert metainfo.children == [
        BinOp(Key(Token(TokenTypes.KEY, 'course')), Token(TokenTypes.KEY_SEPARATOR, ':'), Value(Token(TokenTypes.VALUE, 'Functional Programming'))),
        BinOp(Key(Token(TokenTypes.KEY, 'programLanguage')), Token(TokenTypes.KEY_SEPARATOR, ':'), Value(Token(TokenTypes.VALUE, 'Haskell'))),
        BinOp(Key(Token(TokenTypes.KEY, 'topicTest')), Token(TokenTypes.KEY_SEPARATOR, ':'), Value(Token(TokenTypes.VALUE, 'Standard types'))),
        BinOp(Key(Token(TokenTypes.KEY, 'date')), Token(TokenTypes.KEY_SEPARATOR, ':'), Value(Token(TokenTypes.VALUE, '2023.03.09'))),
    ]



def test_lexer_parse_question():
    question = """
-- newQuestion
-- itemType:txtLn
-- beginCode

x `compr` y 
  | x < y = LT
  | x > y = GT
  | otherwise = EQ
r = ((1::Int) `compr`)

-- endCode

-- ?begin
-- Що буде результатом завантаження коду і виконання команди
-- > True == otherwise
-- ?end


-- !begin
-- = True
-- !end

-- beginHint
-- 'otherwise :: Bool', module Prelude
-- endHint
-- endQuestion
"""
    
    lexer = Lexer(question)
    parser = Parser(lexer)

    parsed_question = parser.item()

    assert parsed_question.children == [
        BinOp(Key(Token(TokenTypes.KEY, 'itemType')), Token(TokenTypes.KEY_SEPARATOR, ':'), Value(Token(TokenTypes.VALUE, 'txtLn'))),
        Compound(name='code').add_children([Value(Token(TokenTypes.VALUE, 'x `compr` y\n| x < y = LT\n| x > y = GT\n| otherwise = EQ\nr = ((1::Int) `compr`)'))]),
        Compound(name='question').add_children([Value(Token(TokenTypes.VALUE, 'Що буде результатом завантаження коду і виконання команди\n> True == otherwise'))]),
        Compound(name='answer').add_children([Value(Token(TokenTypes.VALUE, '= True'))]),
        Compound(name='hint').add_children([Value(Token(TokenTypes.VALUE, "'otherwise :: Bool', module Prelude"))]),
    ]
                
def test_parse_all():
    with open('tests/test.format.example.hs', 'r') as f:
        text = f.read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    compiler = Compiler(parser)
    compiler.compile()
    print(compiler.state)
