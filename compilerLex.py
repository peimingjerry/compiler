
import ply.lex as lex

reserved = {
    'if' : 'IF',
    'else' :  'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'int' : 'INT',
    'char' : 'CHAR',
    'class' : 'CLASS',
}

tokens = [
    'OBJECT_MEMBERSHIP',
    'POINTER_MEMBERSHIP',
    'NUMBER',
    'EQUAL',
    'ASSIGN',
    'INCLUDE',
    'STRING',
    'ID',
] + list(reserved.values())

literals = "+-*/{}()[],;"

t_OBJECT_MEMBERSHIP = r'\.'
t_POINTER_MEMBERSHIP = r'->'

#t_OPERATOR = r'[\+\-\*/]'
t_EQUAL = r'=='
t_ASSIGN = r'='
t_INCLUDE = r'\#include'
t_STRING = r'"[^"]+"'

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_]+[0-9a-zA-Z_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_space(t):
    r'[ \t]+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_comments(t):
    r'//.*\n'
    #print 'comments:', t.value[0:(len(t.value)-1)]

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


