#!/usr/bin/env python
import sys
import pickle
import re
import regex
from regex import RegEx

import lex
import yacc


def buildRE(re_string):
    re = RegEx(regex.EMPTY_STRING)
    count_paranthesis = 0
    check_wobbly = 0
    check_straight = 0

    if re_string == "":
        return RegEx(regex.EMPTY_STRING)
    for i, c in enumerate(re_string):
        if c == '}':
            check_wobbly = 0
            continue
        if c == ']':
            check_straight = 0
            continue

        if check_wobbly == 0 and check_straight == 0:
            if c == '(':
                if count_paranthesis == 0:
                    re = RegEx(regex.CONCATENATION, re, buildRE(re_string[i+1:]))
                count_paranthesis += 1
                continue
            if c == ')':
                count_paranthesis -= 1
                if count_paranthesis < 0:
                    return re
                continue
            if count_paranthesis > 0:
                continue
            if c == '{':
                check_wobbly = 1
                aux = re_string[i+1:]
                aux = aux[:aux.index('}')]
                aux = aux.split(',')
                if len(aux) == 2:
                    if aux[0] != '' and aux[1] != '':
                        aux = (int(aux[0]), int(aux[1]))
                    if aux[0] == '':
                        aux = (-1, int(aux[1]))
                    if aux[1] == '':
                        aux = (int(aux[0]), -1)
                else:
                    aux = (int(aux[0]), int(aux[0]))
                re = RegEx(regex.RANGE, re, aux)
                continue

            if c == '[':
                check_straight = 1
                aux = re_string[i+1:]
                aux = aux[:aux.index(']')]
                new_set = []
                for k, j in enumerate(aux):
                    if aux[k-1] == '-':
                        continue
                    if j != '-':
                        new_set.append(j)
                    if j == '-':
                        new_set.append((new_set.pop(), aux[k+1]))
                        continue
                re = RegEx(regex.SYMBOL_SET, new_set)
                continue

            if c == '|':
                return RegEx(regex.ALTERNATION, re, buildRE(re_string[i+1:]))
            if c == '*':
                if re.type in regex._UNARY_TYPES or re.type in regex._SIMPLE_TYPES:
                    re = RegEx(regex.STAR, re)
                else:
                    re = RegEx(re.type, re.lhs, RegEx(regex.STAR, re.rhs))
                continue
            if c == '+':
                if re.type in regex._UNARY_TYPES or re.type in regex._SIMPLE_TYPES:
                    re = RegEx(regex.PLUS, re)
                else:
                    re = RegEx(re.type, re.lhs, RegEx(regex.PLUS, re.rhs))
                continue
            if c == '?':
                if re.type in regex._UNARY_TYPES or re.type in regex._SIMPLE_TYPES:
                    re = RegEx(regex.MAYBE, re)
                else:
                    re = RegEx(re.type, re.lhs, RegEx(regex.MAYBE, re.rhs))
                continue
            if re.type != regex.EMPTY_STRING:
                if c == '.':
                    re = RegEx(regex.CONCATENATION, re, RegEx(regex.SYMBOL_ANY))
                else:
                    re = RegEx(regex.CONCATENATION, re, RegEx(regex.SYMBOL_SIMPLE, c))
            else:
                if c == '.':
                    re = RegEx(regex.SYMBOL_ANY)
                else:
                    re = RegEx(regex.SYMBOL_SIMPLE, c)
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
        parsed_regex = buildRE(regex_string)

        if sys.argv[1] == "PARSE":
            print(str(parsed_regex))
            sys.exit(0)

    print(parsed_regex.__str__())

    with open(sys.argv[3], "r") as fin:
        content = fin.readlines()
    for word in content:
        pass
        
    print()