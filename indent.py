#!/usr/bin/python
"""
An indentation based array parser written in PLY (Python Lex and Yacc)
Author: Matt Donahoe
2012-12-09

I was curious how lex would handle the "off-side rule".
I had to create a two stage lexer:
The first is the regular lexer in lex.py
The second has a buffer of tokens and a stack of indentation levels.

The indentation logic is based off of Python's
http://docs.python.org/2/reference/lexical_analysis.html#indentation

OTHER RESOURCES

Lexing Python
http://erezsh.wordpress.com/2008/07/12/python-parsing-1-lexing/

Off-side Rule
http://en.wikipedia.org/wiki/Off-side_rule


See GardenSnake.py in PLY's examples for a more complete version I found.

"""
from ply import lex, yacc
from sys import stdin, argv
import copy

# FIRST LEXING STAGE
tokens = (
    'STRING',
    'WHITESPACE',
)

t_STRING = r'[^ \n][^\n]*'
t_WHITESPACE = r'\n[ ]*'

# empty lines dont affect indentation
t_ignore = r'\n[ ]*\n'

def t_error(t):
    print 'error! %s' % t

# create our first stage
lexer = lex.lex()

# SECOND STAGE
class IndentLexer(object):
    """
    A second lexing stage that interprets WHITESPACE
    Manages Off-Side Rule for indentation
    """
    def __init__(self, lexer):
        self.indents = [0]  # indentation stack
        self.tokens = []    # token queue
        self.lexer = lexer

    def input(self, *args, **kwds):
        self.lexer.input(*args, **kwds)

    # Iterator interface
    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next

    def token(self):
        # empty our buffer first
        if self.tokens:
            return self.tokens.pop(0)

        # loop until we find a valid token
        while 1:
            # grab the next from first stage
            token = self.lexer.token()

            # we only care about whitespace
            if not token or token.type != 'WHITESPACE':
                return token

            # check for new indent/dedent
            whitespace = token.value[1:]  # strip \n
            change = self._calc_indent(whitespace)
            if change:
                break

        # indentation change
        if change == 1:
            token.type = 'INDENT'
            return token

        # dedenting one or more times
        assert change < 0
        change += 1
        token.type = 'DEDENT'

        # buffer any additional DEDENTs
        while change:
            self.tokens.append(copy.copy(token))
            change += 1

        return token

    def _calc_indent(self, whitespace):
        "returns a number representing indents added or removed"
        n = len(whitespace) # number of spaces
        indents = self.indents # stack of space numbers
        if n > indents[-1]:
            indents.append(n)
            return 1

        # we are at the same level
        if n == indents[-1]:
            return 0

        # dedent one or more times
        i = 0
        while n < indents[-1]:
            indents.pop()
            if n > indents[-1]:
                raise SyntaxError("wrong indentation level")
            i -= 1
        return i

# create the second stage
lexer = IndentLexer(lexer)

# PARSING STAGE

def p_array(p):
    """array : INDENT elements DEDENT"""
    p[0] = p[2]

def p_elements(p):
    "elements : elements element"
    p[0] = p[1] + [p[2]]

def p_elements_one(p):
    "elements : element"
    p[0] = [p[1]]

def p_element(p):
    """element : STRING
               | array"""
    p[0] = p[1]

def p_error(p):
    print 'p error %s' % p

if __name__ == '__main__':

    from sys import argv, stdin
    x = stdin.read()
    if len(argv) > 1 and argv[1] == 'lex':
        # lex only
        lexer.input(x)
        for t in lexer:
            if t.type == 'STRING':
                print 'STRING:' + t.value
            else:
                print t.type
    else:
        # lex and parse
        print yacc.yacc().parse(x, lexer)

