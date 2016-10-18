ply-playground
========

This repo is my testing grounds for learning [PLY](http://www.dabeaz.com/ply/)

##Setup
 `git submodule init`
 `git submodule update`


##Example parsers

- json.py : a custom json parser
    `cat data/test.json | python json.py`

- plist.py : a custom plist file parser
    `cat data/test.plit | python plist.py`

- indent.py: a demo of parsing a language with significant whitespace
    `cat data/test.indent | python indent.py`


##Lex-Yacc Resources

I have browsed many links that were useful for learning Lex and Yacc. Here are a few:

1. [Backus-Naur Form](http://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form#Software_using_BNF)
1. [Parsing Python](http://erezsh.wordpress.com/2008/07/12/python-parsing-1-lexing/)
1. [Lex/Yacc or Hand Code?](http://erezsh.wordpress.com/2008/07/12/python-parsing-1-lexing/)

