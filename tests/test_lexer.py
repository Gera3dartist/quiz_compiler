from src.ast_parser import Lexer, Token, TokenTypes

def test_lexer_parse_meta_comments():
    meta_comment = """
--- 
--- Все, що за '---', ігноруюється, як коментар.
--- Порожні рядки ігноруюються, за винятком коду, 
---         тобто між -- beginCode та -- endCode не ігноруються.
"""
    print('testing')
    lines = [l.strip() for l in meta_comment.splitlines() if l.strip() != '']
    lexer = Lexer(meta_comment)
    assert lexer.get_next_token() == Token(TokenTypes.META_COMMENT, lines[0])
    assert lexer.get_next_token() == Token(TokenTypes.META_COMMENT, lines[1])
    assert lexer.get_next_token() == Token(TokenTypes.META_COMMENT, lines[2])
    assert lexer.get_next_token() == Token(TokenTypes.META_COMMENT, lines[3])

def test_lexer_parse_metadata():
    metadata = """
-- course: Functional Programming
-- programLanguage: Haskell
-- topicTest:  Standard types
-- date: 2023.03.09
"""
    res = [
        Token(TokenTypes.KEY, 'course'),
        Token(TokenTypes.KEY_SEPARATOR, ':'),
        Token(TokenTypes.VALUE, 'Functional Programming'),
        Token(TokenTypes.KEY, 'programLanguage'),
        Token(TokenTypes.KEY_SEPARATOR, ':'),
        Token(TokenTypes.VALUE, 'Haskell'),
        Token(TokenTypes.KEY, 'topicTest'),
        Token(TokenTypes.KEY_SEPARATOR, ':'),
        Token(TokenTypes.VALUE, 'Standard types'),
        Token(TokenTypes.KEY, 'date'),
        Token(TokenTypes.KEY_SEPARATOR, ':'),
        Token(TokenTypes.VALUE, '2023.03.09'),
    ]

    lexer = Lexer(metadata)
    for token in res:
        assert lexer.get_next_token() == token


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
    question = question * 2
    res = [
        Token(TokenTypes.BLOCK_START, "newQuestion"),
        Token(TokenTypes.KEY, "itemType"),
        Token(TokenTypes.KEY_SEPARATOR, ":"),
        Token(TokenTypes.VALUE, "txtLn"),
        Token(TokenTypes.BLOCK_START, "beginCode"),
        Token(TokenTypes.VALUE, "x `compr` y"),
        Token(TokenTypes.VALUE, "| x < y = LT"),
        Token(TokenTypes.VALUE, "| x > y = GT"),
        Token(TokenTypes.VALUE, "| otherwise = EQ"),
        Token(TokenTypes.VALUE, "r = ((1::Int) `compr`)"),
        Token(TokenTypes.BLOCK_END, "endCode"),
        Token(TokenTypes.BLOCK_START, "?begin"),
        Token(TokenTypes.VALUE, "Що буде результатом завантаження коду і виконання команди"),
        Token(TokenTypes.VALUE, "> True == otherwise"),
        Token(TokenTypes.BLOCK_END, "?end"),
        Token(TokenTypes.BLOCK_START, "!begin"),
        Token(TokenTypes.VALUE, "= True"),
        Token(TokenTypes.BLOCK_END, "!end"),
        Token(TokenTypes.BLOCK_START, "beginHint"),
        Token(TokenTypes.VALUE, "'otherwise :: Bool', module Prelude"),
        Token(TokenTypes.BLOCK_END, "endHint"),
        Token(TokenTypes.BLOCK_END, "endQuestion"),
    ] * 2

    lexer = Lexer(question)
    for token in res:
        assert lexer.get_next_token() == token
