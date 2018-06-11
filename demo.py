# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------
import sys

# 词法分析器生成器
import ply.lex as lex

# 语法分析器生成器
import ply.yacc as yacc

# 判断是否使用python3
if sys.version_info[0] >= 3:
    raw_input = input

# 新建元祖
tokens = (
    'NAME', 'NUMBER',
)

# 新建list列表数据类型
literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens
# 加r表示这个string是一个raw string,不转义
# 正则表达式
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


# 定义一个方法,
# 正则表达式匹配所有数字
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# 忽略tab键的正则表达式？
t_ignore = " \t"


# 忽略换行符
# count:计算换行符出现的次数
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Build the lexer

lex.lex()


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}


def p_statement_assign(p):
    'statement : NAME "=" expression'
    names[p[1]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
