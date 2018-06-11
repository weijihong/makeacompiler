import ply.lex as lex
import ply.yacc as yacc
import sys

# 词法单元类型列表
tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS'
]

# 词法单元模式描述
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='

# 丢弃匹配的token
t_ignore = r' '


def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


# t is a token object
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t


def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1)


# 构建词法分析器
lexer = lex.lex()

lexer.input("1+2")




while True:
    # 返回识别出的下一个token，如果解析完毕返回None
    tok = lexer.token()
    if not tok:
        break
    print(tok)
