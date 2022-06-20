import ply.lex as lex

#CREATE [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { ivent [ OR ... ] }
#    ON table_name
#    [ FROM table_name ]
#    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
#    [ FOR [ EACH ] { ROW | STATEMENT } ]
#    [ WHEN ( condition ) ]
#    EXECUTE PROCEDURE function_name ( arguents )
#Where ivent is:
#    INSERT
#    UPDATE [ OF column_name [, ... ] ]
#    DELETE
#    TRUNCATE

tokens = ("CREATE","CONSTRAINT","TRIGGER","NAME","BEFORE","AFTER","INSTEADOF",
        "INSERT","UPDATE","OF","DELETE","TRUNCATE","OR","ON","FROM","NOTDEFERRABLE",
       "DEFERRABLE","INITIALLYIMMEDIATE","INITIALLYDEFERRED","FOR","EACH",
        "ROW","STATEMENT","WHEN","CONDITION","EXECUTEPROCEDURE","ARGUMENT","COMMA",
        "LS","RS","EXP_END")

ident = r'[a-z]\w*'
t_ignore = ' \t'
t_CREATE = r"\CREATE"
t_CONSTRAINT = r"\CONSTRAINT"
t_TRIGGER = r"\TRIGGER"
t_NAME = ident
t_BEFORE = r"\BEFORE"
t_AFTER = r"\AFTER"
t_INSTEADOF = r'INSTEAD[ ]+OF'
t_INSERT = r"\INSERT"
t_UPDATE = r"\UPDATE"
t_OF = r"\OF"
t_DELETE = r"\DELETE"
t_TRUNCATE = r"\TRUNCATE"
t_OR = r"\OR"
t_ON = r"\ON"
t_FROM = r"\FROM"
t_NOTDEFERRABLE = r'\NOT[ ]+DEFERRABLE'
t_DEFERRABLE = r"\DEFERRABLE"
t_INITIALLYIMMEDIATE = r'\INITIALLY[ ]+IMMEDIATE'
t_INITIALLYDEFERRED = r'\INITIALLY[ ]+DEFERRED'
t_FOR = r"\FOR"
t_EACH = r"\EACH"
t_ROW = r"\ROW"
t_STATEMENT = r"\STATEMENT"
t_WHEN = r"\WHEN"
t_CONDITION = r'\"\'\w*(<|>|=|(!=)|(==)|(>=)|(<=))\w*|\w*\'\"'
t_EXECUTEPROCEDURE = r'\EXECUTE[ ]+PROCEDURE'
t_ARGUMENT = r'\'[a-zA-Z0-9]*\''
t_COMMA = r'\,'
t_LS = r'\('
t_RS = r'\)'
t_EXP_END = r'\;'



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print('Illegal character {0}'.format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

import ply.yacc as yacc

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append(str(part))
        return "\n".join(st)

    def __repr__(self):
        return self.type + "|" + self.parts_str().replace("\n", "\n|")

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

def p_create(p):
    '''create : CREATE constraint TRIGGER NAME baio_ivent ON NAME with_params EXECUTEPROCEDURE NAME argument EXP_END'''
    p[0] = Node('', [p[1], p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11]])

def p_constraint (p):
    ''' constraint :
            | CONSTRAINT'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1]])

def p_baio_ivent (p):
    ''' baio_ivent : baio ivent_or'''
    p[0] = Node('', [p[1]])

def p_baio (p):
    ''' baio : BEFORE
            | AFTER
            | INSTEADOF'''
    p[0] = Node('', [p[1]])

def p_ivent_or (p):
    ''' ivent_or : ivent or'''
    p[0] = Node('', [p[1], p[2]])

def p_ivent (p):
    ''' ivent : INSERT
            | DELETE
            | TRUNCATE
            | update_of'''
    p[0] = Node('', [p[1]])

def p_or (p):
    '''or :
            | OR ivent_or'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_update_of (p):
    '''update_of : UPDATE of_name'''
    p[0] = Node('', [p[1],p[2]])

def p_of_name (p):
    '''of_name : OF name_comma'''
    p[0] = Node('', [p[1], p[2]])

def p_name_comma (p):
    '''name_comma : NAME comma'''
    p[0] = Node('', [p[1], p[2]])

def p_comma (p):
    '''comma :
            | COMMA name_comma'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_with_params (p):
    '''with_params :
            | from nddiiid for when'''
    if len(p) == 1:
        p[0] = Node('', ['None params'])
    else:
        p[0] = Node('', [p[1],p[2],p[3],p[4]])

def p_from (p):
    '''from :
            | FROM NAME'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_nddiiid (p):
    '''nddiiid :
            | ndef_def ii_id'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_ndef_def (p):
    '''ndef_def : NOTDEFERRABLE
            | DEFERRABLE'''
    p[0] = Node('',[p[1]])

def p_ii_id (p):
    '''ii_id :
            | INITIALLYIMMEDIATE
            | INITIALLYDEFERRED'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1]])

def p_for (p):
    '''for :
            | FOR each row_stat'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_each (p):
    '''each :
            | EACH'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1]])

def p_row_stat (p):
    '''row_stat : ROW
            | STATEMENT'''
    p[0] = Node('',[p[1]])

def p_when (p):
    '''when :
            | WHEN CONDITION'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_argument (p):
    '''argument : LS arg_comma RS'''
    p[0] = Node('', [p[1], p[2],p[3]])

def p_arg_comma (p):
    '''arg_comma :
            | NAME a_comma'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_a_comma (p):
    '''a_comma :
            | COMMA arg_comma'''
    if len(p) == 1:
        p[0] = Node('', [''])
    else:
        p[0] = Node('', [p[1], p[2]])

def p_error(p):
    print('syntax error in line {0}'.format(p.lineno))
    yacc.errok()

yacc.yacc()

data ='''CREATE TRIGGER check_update BEFORE INSERT FOR EACH ROW EXECUTE PROCEDURE check_account_update();'''

if __name__ == '__main__':
    print("Data:\n", data, "\n\nLex analize:")

    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

    print("\nYacc analize:")
    result = yacc.parse(data)
    print(result)

    print("No errors in lex and yacc.")
