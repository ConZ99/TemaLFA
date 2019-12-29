#!/usr/bin/env python
import sys
import pickle
import re
from regex import RegEx

import string


CHARSET = string.digits + string.ascii_letters

EMPTY_STRING = 0
SYMBOL_SIMPLE = 1
SYMBOL_ANY = 2
SYMBOL_SET = 3
MAYBE = 4
STAR = 5
PLUS = 6
RANGE = 7
CONCATENATION = 8
ALTERNATION = 9

_SIMPLE_TYPES = {EMPTY_STRING, SYMBOL_SIMPLE, SYMBOL_ANY, SYMBOL_SET}
_BINARY_TYPES = {CONCATENATION, ALTERNATION}

def buildRE(re_string):
    
    return re

if __name__ == "__main__":
    valid = (len(sys.argv) == 4 and sys.argv[1] in ["RAW", "TDA"]) or \
            (len(sys.argv) == 3 and sys.argv[1] == "PARSE")
    if not valid:
        sys.stderr.write(
            "Usage:\n"
            "\tpython3 main.py RAW <regex-str> <words-file>\n"
            "\tOR\n"
            "\tpython3 main.py TDA <tda-file> <words-file>\n"
            "\tOR\n"
            "\tpython3 main.py PARSE <regex-str>\n"
        )
        sys.exit(1)

    if sys.argv[1] == "TDA":
        tda_file = sys.argv[2]
        with open(tda_file, "rb") as fin:
            parsed_regex = pickle.loads(fin.read())
    else:
        regex_string = sys.argv[2]

        # TODO "regex_string" conține primul argument din linia de comandă,
        # șirul care reprezintă regexul cerut. Apelați funcția de parsare pe el
        # pentru a obține un obiect RegEx pe care să-l stocați în
        # "parsed_regex"
        #
        # Dacă nu doriți să implementați parsarea, puteți ignora această parte.

        parsed_regex = buildRE(regex_string)

        if sys.argv[1] == "PARSE":
            print(str(parsed_regex))
            sys.exit(0)


    with open(sys.argv[3], "r") as fin:
        content = fin.readlines()
    for word in content:

        p = re.compile(regex_string+'\n')
        print(str(bool(p.fullmatch(word))))
        # TODO la fiecare iterație, "word" conținue un singur cuvânt din
        # fișierul de input; verificați apartenența acestuia la limbajul
        # regexului dat și scrieți rezultatul la stdout.
    print()