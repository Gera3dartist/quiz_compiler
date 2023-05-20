'''
-- newQuestion
-- itemType = txtLn
-- beginCode

x `compr` y 
  | x < y = LT
  | x > y = GT
  | otherwise = EQ

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
-------------------------------------------------
'''
from dataclasses import dataclass


@dataclass
class Question:
    item_type: str
    code_block: str
    question_block: str
    answer_block: str
    hint_block: str

    def __init__(self, item_type):
        pass
