-- course: 
-- programLanguage: 
-- topicTest:  
-- date: 

-- beginAnnonce
-- endAnnonce

--------------

-- newQuestion
-- itemType:

-- beginCode
-- 
-- endCode

-- ?begin
-- 
-- ?end


-- !begin
-- 
-- !end

-- beginHint
-- 
-- endHint
-------------------------------------------------

--- Приклад - у файлі 'Тест.формат.приклад.hs'.

--- За цим прикладом на локальному комп'ютері створюється проєкт з такою,наприклад, структурою

---     Можливо Tests і FP_Haskell уже існують
---  └─ Tests
---     └─ FP_Haskell
---        ├─ listOfTests.txt
---        │    тут додається запис  "TN:4; testName:Standard_types_2023.03.09; NQ: 24; " 
---        │        тобто  згенеровано тест № 4, назва - Standard_types_2023.03.09, кількість питань - 24(NQ - number of questions)
---        └─ Standard_types_2023.03.09
---           ├─ testGeneratorTN.gs
---           │    тут - код для генерування варіантів тесту у вигляді Google Forms,
---           │           тобто пункт 2.3 Завдання
---           ├── qstTN
---           │   ├─ 1qstTN.txt
---           │   ├─ ...
---           │   ├─ 10qstTN.txt
---           │   ├─ ...
---           │   └─ NqstTN.txt
---           ├── answTN
---           │   ├─ 1answTN.txt
---           │   ├─ ...
---           │   ├─ 10answTN.txt
---           │   ├─ ...
---           │   └─ NanswTN.txt
---           ├── hintTN
---           │   ├─ 1hintTN.txt
---           │   ├─ ...
---           │   ├─ 10hintTN.txt
---           │   ├─ ...
---           │   └─ NhintTN.txt
---           ├── codeTN
---           │   ├─ 1codeTN.hs
---           │   ├─ ...
---           │   ├─ 10codeTN.hs
---           │   ├─ ...
---           │   └─ NcodeTN.hs
---           └── imgTN
---               ├─ 1imgTN.hs.png
---               ├─ ...
---               ├─ 10imgTN.hs.png
---               ├─ ...
---               └─ NimgTN.hs.png

Тепер, наприклад, папка Standard_types_2023.03.09 завантажується на Google Диск, там запускається функція genTests4() з testGeneratorTN.gs і генеруються форми + текстовий файл-журнал.
Для конвертації коду у формат .png я використав бібліотеку PIL, файл txt2im.01.py.

Надіслані матеріали не містять самого компілятора, проте приклад працюючий, тобто форми генеруються.
Все решта - при усному обговоренні. 

--
Приклад генерування форм з google таблиць. Там і інші типи питань 
https://github.com/surajp/sheettoform/blob/master/SheetToForm.gs