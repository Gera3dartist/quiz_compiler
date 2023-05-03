--- 
--- Все, що за '---', ігноруюється, як коментар.
--- Порожні рядки ігноруюються, за винятком коду, 
---         тобто між -- beginCode та -- endCode не ігноруються.

--- Метадані
-- course: Functional Programming
-- programLanguage: Haskell
-- topicTest:  Standard types
-- date: 2023.03.09

-- beginAnnonce
-- Наданий код розглядається в припущенні, що завантажені модулі Prelude та Data.Monoid
-- Помилку часу компіляції позначаємо у відповідях словом err1
-- Винятки часу виконання (bottom) позначаємо словом err2
-- endAnnonce

--------------

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

-- newQuestion
-- itemType = txtLn
--beginCode

x `compr` y 
  | x < y = LT
  | x > y = GT
  | otherwise = EQ

--endCode

-- ?begin
-- Що буде результатом завантаження коду і виконання команди
-- > compr 123 123
-- ?end


-- !begin
-- = EQ
-- !end

-- beginHint
-- 'data Ordering', module Prelude
-- 'охороннi вирази', 'Неформальний вступ'
-- endHint
-------------------------------------------------

-- newQuestion
-- itemType = txtLn
--beginCode

x `compr` y 
  | x < y = LT
  | x > y = GT
  | otherwise = EQ

r = ((1::Int) `compr`)

--endCode

-- ?begin
-- Вкажіть сигнатуру типів функції r
-- ?end


-- !begin
-- = r :: Int -> Ordering
-- !end

-- beginHint
-- Розділ '3.5 Sections', Haskell 2010 Language Report
-- endHint
-------------------------------------------------

-- newQuestion
-- itemType = txtLn
--beginCode

fn [] = []
fn (x:ys) = [x,x] : fn ys

result = concat $ fn [1..3]
--endCode

-- ?begin
-- Вкажіть сигнатуру типів функції fn
-- ?end


-- !begin
-- = fn :: [a] -> [[a]]
-- !end

-- beginHint
-- 'List operations', module Prelude
-- endHint
-------------------------------------------------

-- newQuestion
-- itemType = txtLn
--beginCode

fn s [] = s
fn s (x:ys) = [x,x] ++ fn s ys

--endCode

-- ?begin
-- Вкажіть сигнатуру типів функції fn
-- ?end


-- !begin
-- = fn :: [a] -> [a] -> [a]
-- !end

-- beginHint
-- 'List operations', module Prelude
-- endHint
-------------------------------------------------

-- newQuestion
-- itemType = txtLn
--beginCode

fmf = flip fmap

result = fmf [1..3]

--endCode

-- ?begin
-- Визначте сигнатуру типів функції fmf
-- ?end


-- !begin
-- = fmf :: [a] -> (a -> b) -> [b]
-- !end

-- beginHint
-- 'List operations', module Prelude
-- 'Miscellaneous functions', module Prelude
-- endHint
-------------------------------------------------

-- newQuestion
-- itemType = txtLn
--beginCode

fmf = flip fmap

result = fmf [1..3]

--endCode

-- ?begin
-- Вкажіть арність функції result (числом, наприклад 5)
-- ?end


-- !begin
-- = 1
-- !end

-- beginHint
-- 'арність', 'Неформальний вступ'
-- 'List operations', module Prelude
-- 'Miscellaneous functions', module Prelude
-- endHint
-------------------------------------------------

-- newQuestion
-- itemType = txtLn
--beginCode

fmf = flip fmap

result = fmf ([1..3]::[Float])

--endCode

-- ?begin
-- Вкажіть сигнатуру типів функції result
-- ?end


-- !begin
-- = result :: (Float -> a) -> [a]
-- !end

-- beginHint
-- 'List operations', module Prelude
-- 'Miscellaneous functions', module Prelude
-- endHint
-------------------------------------------------