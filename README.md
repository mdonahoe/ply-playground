plexyacc
========

Plexyacc is my playground for learning Lex and Yacc.

Currently I am using [PLY](http://www.dabeaz.com/ply/),
but I may switch to the original lex and yacc in the future.

I have a few test parsers that I am working on.

#Goal
A goal of mine is to create an Xcode project file linter.
Git frequently ruins .pbxproj files during merges,
and Xcode will refuse to open them. There exists a plutil command for Mac OSX,
but I can't seem to get it to tell me where my file is busted.

My goal is to leverage the whitespace structure of auto-generated .pbxproj files
to help pinpoint errors.

#Resources

I have acquired many many links that were useful for learnign Lex and Yacc

1. [Backus-Naur Form](http://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form#Software_using_BNF)
1. [Parsing Python](http://erezsh.wordpress.com/2008/07/12/python-parsing-1-lexing/)
1. [Lex/Yacc or Hand Code?](http://erezsh.wordpress.com/2008/07/12/python-parsing-1-lexing/)

