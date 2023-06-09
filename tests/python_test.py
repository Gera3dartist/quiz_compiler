## 
## Все, що за '##', ігноруюється, як коментар.
## Порожні рядки ігноруюються, за винятком коду, 
##         тобто між # beginCode та # endCode не ігноруються.

## Метадані
# course: Functional Programming
# programLanguage: Haskell
# topicTest:  Standard types
# date: 2023.03.09

# beginAnnonce
# Наданий код розглядається в припущенні, що завантажені модулі Prelude та Data.Monoid
# Помилку часу компіляції позначаємо у відповідях словом err1
# Винятки часу виконання (bottom) позначаємо словом err2
# endAnnonce

#######

# newQuestion
# itemType :txtLn
# beginCode

student = {
    "name": "John",
    "age": 20,
    "grade": "A"
}
print(student["name"])


# endCode

# ?begin
# What will be printed to the console when this code is executed?
# > True == otherwise
# ?end


# !begin
# = True
# !end

# beginHint
# 'otherwise :: Bool', module Prelude
# endHint
# endQuestion

# newQuestion
# itemType :txtLn
# beginCode

numbers = [1, 2, 3, 4, 5]
squared_numbers = [x**2 for x in numbers]
print(squared_numbers)

# endCode

# ?begin
# What is the value that will be printed to the console?
# > True == otherwise
# ?end


# !begin
# = True
# !end

# beginHint
# 'otherwise :: Bool', module Prelude
# endHint
# endQuestion
