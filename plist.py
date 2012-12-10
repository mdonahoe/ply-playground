#!/usr/bin/python
"""
plist.py
A plist parser written in PLY (Python Lex and Yacc)
Author: Matt Donahoe
2012-12-08

Probably buggy as hell
"""
from ply import lex, yacc
from sys import stdin, argv

tokens = (
    'STRING',
    'A_BEGIN','A_END',
    'O_BEGIN','O_END',
    'LINECOMMENT',
    'BLOCKCOMMENT',
    'COMMA',
    'EQUALS',
    'SEMICOLON',
    'WHITESPACE',
)

"string"
HEX_DIGIT     = "[0-9a-f]"
UNESCAPEDCHAR = "[ -!#-\[\]-~]"  # ASCII codes 32-127, except " and \
ESCAPEDCHAR   = r'\\["\\bfnrt/]'
UNICODECHAR   = r'\\u' + HEX_DIGIT + HEX_DIGIT + HEX_DIGIT + HEX_DIGIT
CHAR          = (UNESCAPEDCHAR +
                "|" + ESCAPEDCHAR +
                "|" + UNICODECHAR)

t_STRING = r'"('+CHAR+')*"|[\w\./]+'

t_EQUALS      = "="
t_A_BEGIN     = "\("
t_A_END       = "\)"
t_O_BEGIN     = "\{"
t_O_END       = "\}"
t_COMMA       = ","
t_SEMICOLON   = ";"

def t_WHITESPACE(t):
    r'[\n\t\r ]'
    pass

def t_LINECOMMENT(t):
    r'//.*\n'
    #print 'got a comment', t
    pass

def t_BLOCKCOMMENT(t):
    r'/\*(.+?)\*/'
    #print 'got a comment', t
    pass

def t_error(t):
    print "illegal at %s" % t.value[0:3]
    t.lexer.skip(1)

# Now create the lexer.
# It will examine this context and find all these constants
lexer = lex.lex()

def parse_string(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s

# Parsing functions
def p_value_string(p):
    "value : STRING"
    p[0] = parse_string(p[1])

def p_value_container(p):
    """value : array
             | object"""
    p[0] = p[1]

def p_array(p):
    "array : A_BEGIN elements A_END"
    p[0] = p[2]

def p_empty_array(p):
    "array : A_BEGIN A_END"
    p[0] = []

def p_object(p):
    "object : O_BEGIN members O_END"
    p[0] = dict(p[2])

def p_empty_object(p):
    "object : O_BEGIN O_END"
    p[0] = {}

def p_elements(p):
    "elements : value COMMA elements"
    p[0] = [p[1]] + p[3]

def p_one_element(p):
    "elements : value"
    p[0] = [p[1]]

def p_one_element_with_comma(p):
    "elements : value COMMA"
    p[0] = [p[1]]

def p_members(p):
    "members : pair members"
    p[0] = [p[1]] + p[2]

def p_one_member(p):
    "members : pair"
    p[0] = [p[1]]

def p_pair(p):
    "pair : STRING EQUALS value SEMICOLON"
    key = parse_string(p[1])
    p[0] = (key, p[3])

def p_error(p):
    if p is None:
        print 'Ran out of input.'
        return
    print 'err: %s' % p

Y = yacc.yacc()
if __name__ == '__main__':
    x = stdin.read()
    if len(argv) > 1 and argv[1] == 'lex':
        lexer.input(x)
        print '\n'.join([t.type for t in lexer])
    else:
        print Y.parse(x)
