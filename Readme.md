Referrences:
1. [EBNF reference][https://www.ics.uci.edu/~pattis/ICS-33/lectures/ebnf.pdf]
2. [GRAMMAR][https://en.wikibooks.org/wiki/Introduction_to_Programming_Languages/Grammars]

Tools:
1. [Working with ebnf][https://github.com/matthijsgroen/ebnf2railroad/tree/main]
2. [Google Admin Site] [https://console.cloud.google.com/apis/api/classroom.googleapis.com/metrics?project=vibrant-arcanum-348221]

API to use:
1. [Google Forms - Question object][https:``//developers.google.com/forms/api/reference/rest/v1/forms#question]
2. [Classroom API][https://developers.google.com/classroom/reference/rest/?apix=true]

Usage.
1. In order to show state:
`python`
2. In order to compile:
`python -m src.manage compile --path /Users/andriigerasymchuk/private-repositories/quiz_compiler/tests/test.format.example.hs
3. Update form with data:
```python
python -m src.manage upload-to-google --form_id 1XndvXhGdXufBqBNwHFyfXwz_hkiie83Px-U5oWvs3zI
```