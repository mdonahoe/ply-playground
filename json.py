"""
A json parser written in PLY (Python Lex and Yacc)
Author: Matt Donahoe
2012-12-08

Heavily influenced by
https://gist.github.com/436828
"""

from ply import lex, yacc
from sys import stdin, argv

# this variable is required
tokens = (
    'STRING',
    'NUMBER',
    'TRUE',
    'FALSE',
    'NULL',
    'A_BEGIN','A_END',
    'O_BEGIN','O_END',
    'COMMA',
    'COLON',
    'WHITESPACE',
)

"number"
INT      = '-?(0|[1-9][0-9]*)'
FRAC     = '(\\.?[0-9]+)?'
EXP      = '([eE][-+]?[0-9]+)?'

# lex searches for this because NUMBER is a token
t_NUMBER = '(' + INT + FRAC + EXP + ')'

"string"
HEX_DIGIT     = "[0-9a-f]"
UNESCAPEDCHAR = "[ -!#-\[\]-~]"  # ASCII codes 32-127, except " and \
ESCAPEDCHAR   = r'\\["\\bfnrt/]'
UNICODECHAR   = r'\\u' + HEX_DIGIT + HEX_DIGIT + HEX_DIGIT + HEX_DIGIT
CHAR          = (UNESCAPEDCHAR +
                "|" + ESCAPEDCHAR +
                "|" + UNICODECHAR)
CHARS         = "(" + CHAR + ")+"
DBL_QUOTE     = '["]'

# lex searches for this because STRING is a token
t_STRING      = (DBL_QUOTE + DBL_QUOTE +
                "|" + DBL_QUOTE + CHARS + DBL_QUOTE)

# these are more tokens
t_TRUE    = "true"
t_FALSE   = "false"
t_NULL    = "null"
t_A_BEGIN = "\["
t_A_END   = "\]"
t_O_BEGIN = "\{"
t_O_END   = "\}"
t_COMMA   = ","
t_COLON   = ":"

# ignore whitespace
# lex looks at the docstring for the pattern
def t_WHITESPACE(t):
    r'[\n\t\r ]'
    pass

def t_error(t):
    print "illegal at %s" % t.value
    t.lexer.skip(1)

# PLY now introspects this file to build the lexer rules
lexer = lex.lex()

# Parsing functions
# Yacc examines the docstring for the rules
def p_value_string(p):
    "value : STRING"
    p[0] = p[1][1:-1]  # remove quotes

def p_value_number(p):
    "value : NUMBER"
    x = float(p[1])
    p[0] = int(x) if x == int(x) else x  # use int if we can

def p_value_container(p):
    """value : array
             | object"""
    p[0] = p[1]

def p_value_bool(p):
    """value : TRUE
             | FALSE"""
    p[0] = p[1] == 'true'

def p_value_null(p):
    "value : NULL"
    p[0] = None

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

def p_members(p):
    "members : pair COMMA members"
    p[0] = [p[1]] + p[3]

def p_one_member(p):
    "members : pair"
    p[0] = [p[1]]

def p_pair(p):
    "pair : STRING COLON value"
    key = p[1][1:-1]  # remove quotes
    p[0] = (key, p[3])

def p_error(p):
    print 'err: %s' % p

# PLY now introspects this file to build the parse rules
Y = yacc.yacc()


# Duplicate some of the real json module's methods
def loads(s):
    "Parse a string"
    return Y.parse(s)

def load(f):
    "Parse a file"
    return loads(f.read())

def dumps(f, obj):
    raise NotImplementedError

def dump(f, obj):
    f.write(dumps(obj))
    f.close()


if __name__ == '__main__':
    x = stdin.read()
    if len(argv) > 1 and argv[1] == 'lex':
        lexer.input(x)
        print '\n'.join([t.type for t in lexer])
    else:
        print Y.parse(x)
